/**
 * KF websites – publish services from KF Ledger
 * ------------------------------------------------
 * Reads the "Service Category" and "Service" tables in KF Ledger and writes each
 * company's active services to its website repository (data/catalog.json).
 * GitHub then rebuilds and republishes that website automatically (1–2 minutes).
 *
 * Add a service in KF Ledger  -> it appears on the website after the next publish.
 * Mark a service inactive      -> it disappears from the website.
 * New company with a website   -> add one line to SITES below.
 *
 * Setup (once):
 *   1. script.google.com -> New project -> paste this file. Name it "KF websites publisher".
 *   2. Project Settings -> Script properties -> add GITHUB_TOKEN
 *      (a fine-grained GitHub token for kf-group with "Contents: Read and write"
 *       on the website repositories only).
 *   3. Run publishAll once and approve the permissions.
 *   4. Optional: run installDailyTrigger to publish automatically every night.
 *
 * This script only READS KF Ledger. It never edits the workbook.
 */

const LEDGER_ID = '18PMXUzfN_KcZ2z5pgtuE7k9G_CBBK_5dH_8M4-1bMrw';

// company_id in KF Ledger  ->  GitHub repository of that company's website
const SITES = {
  'CO-KFS': 'kf-group/kfsecurities-site',
  'CO-KFE': 'kf-group/kfnxt-site'
};

const CATALOG_PATH = 'data/catalog.json';

function publishAll() {
  const ss = SpreadsheetApp.openById(LEDGER_ID);
  const cats = readTable_(ss, 'Service Category');
  const svcs = readTable_(ss, 'Service');
  const log = [];
  Object.keys(SITES).forEach(function (co) {
    const myCats = cats.filter(function (c) { return c.company_id === co && isActive_(c.active); });
    const ids = myCats.map(function (c) { return c.id; });
    const mySvcs = svcs.filter(function (s) { return ids.indexOf(s.category_id) >= 0 && isActive_(s.active) && s.name; });
    const catalog = {
      company_id: co,
      exported: Utilities.formatDate(new Date(), 'Asia/Kolkata', 'yyyy-MM-dd'),
      source: 'KF Ledger (Service Category + Service)',
      categories: myCats.map(function (c) { return { id: c.id, name: c.name }; }),
      services: mySvcs.map(function (s) { return { id: s.id, category_id: s.category_id, name: s.name }; })
    };
    if (!catalog.services.length) { log.push(co + ': no active services in KF Ledger, website left unchanged'); return; }
    const res = putFile_(SITES[co], CATALOG_PATH, JSON.stringify(catalog, null, 1) + '\n', 'Publish services from KF Ledger');
    log.push(co + ' -> ' + SITES[co] + ': ' + res + ' (' + catalog.services.length + ' services)');
  });
  Logger.log(log.join('\n'));
  try { SpreadsheetApp.getUi().alert(log.join('\n')); } catch (e) {}
  return log;
}

function installDailyTrigger() {
  ScriptApp.getProjectTriggers().forEach(function (t) {
    if (t.getHandlerFunction() === 'publishAll') ScriptApp.deleteTrigger(t);
  });
  ScriptApp.newTrigger('publishAll').timeBased().everyDays(1).atHour(2).inTimezone('Asia/Kolkata').create();
}

// ---------- helpers ----------
function isActive_(v) { return String(v || '').trim().toLowerCase() === 'active'; }

function readTable_(ss, name) {
  const sh = ss.getSheetByName(name);
  if (!sh) throw new Error('Sheet not found in KF Ledger: ' + name);
  const v = sh.getDataRange().getDisplayValues();
  const h = v[0].map(function (x) { return String(x).trim(); });
  return v.slice(1).filter(function (r) { return r[0]; }).map(function (r) {
    const o = {}; h.forEach(function (k, i) { o[k] = String(r[i] || '').trim(); }); return o;
  });
}

function putFile_(repo, path, content, message) {
  const token = PropertiesService.getScriptProperties().getProperty('GITHUB_TOKEN');
  if (!token) throw new Error('Add GITHUB_TOKEN in Project Settings -> Script properties');
  const url = 'https://api.github.com/repos/' + repo + '/contents/' + path;
  const headers = { Authorization: 'Bearer ' + token, Accept: 'application/vnd.github+json' };
  let sha = null, old = null;
  const g = UrlFetchApp.fetch(url, { headers: headers, muteHttpExceptions: true });
  if (g.getResponseCode() === 200) {
    const j = JSON.parse(g.getContentText()); sha = j.sha;
    old = Utilities.newBlob(Utilities.base64Decode(j.content.replace(/\n/g, ''))).getDataAsString();
  }
  // ignore the export date when comparing, so an unchanged Ledger does not trigger a rebuild
  const strip = function (s) { return (s || '').replace(/"exported": "[^"]*"/, ''); };
  if (old !== null && strip(old) === strip(content)) return 'no changes';
  const body = { message: message, content: Utilities.base64Encode(content, Utilities.Charset.UTF_8), branch: 'main' };
  if (sha) body.sha = sha;
  const p = UrlFetchApp.fetch(url, { method: 'put', headers: headers, contentType: 'application/json', payload: JSON.stringify(body), muteHttpExceptions: true });
  if (p.getResponseCode() >= 300) throw new Error(repo + ': GitHub ' + p.getResponseCode() + ' ' + p.getContentText());
  return 'published';
}
