"""Fix the exportCSV function to read from localStorage instead of empty MOCK arrays."""

with open('admin/admin.js', 'r', encoding='utf-8') as f:
    content = f.read()

old_export = """function exportCSV(type) {
  let csv ="";
  switch(type) {
    case "users":
      csv = ["Name,Email,Plan,Joined,Expiry,Status",...MOCK_USERS.map(u=>`${u.name},${u.email},${u.plan},${u.joined},${u.expiry},${u.status}`)].join("\\n");
      break;
    case "payments":
      csv = ["User,Plan,Amount,Reference,Time,Status",...MOCK_PAYMENTS.map(p=>`${p.user},${p.plan},${p.amount},"${p.ref}",${p.time},${p.status}`)].join("\\n");
      break;
    case "support":
      csv = ["Name,Email,Subject,Status,Time",...MOCK_SUPPORT.map(q=>`${q.name},${q.email},${q.subject},${q.status},${q.time}`)].join("\\n");
      break;
    default:
      csv = "No data";
  }
  downloadFile(`${type}_report.csv`, csv, "text/csv");
  showToast(`${type.charAt(0).toUpperCase()+type.slice(1)} report downloaded!`, "success");
}"""

new_export = """function exportCSV(type) {
  let csv ="";
  switch(type) {
    case "users": {
      var udata=[]; try{udata=JSON.parse(localStorage.getItem('ar_accounts')||'[]');}catch{}
      var enriched = udata.map(function(u){ var pr=null; try{pr=JSON.parse(localStorage.getItem('ar_plan_'+u.email.toLowerCase())||'null');}catch{} return {name:u.name||u.email.split('@')[0],email:u.email,plan:pr?pr.plan:'free',joined:u.created?new Date(u.created).toLocaleDateString('en-IN'):'--',expiry:pr&&pr.expiry?new Date(pr.expiry).toLocaleDateString('en-IN'):'--',status:u.suspended?'suspended':(pr&&Date.now()<pr.expiry?'active':(pr?'expired':'free'))}; });
      csv = ["Name,Email,Plan,Joined,Expiry,Status",...enriched.map(u=>`${u.name},${u.email},${u.plan},${u.joined},${u.expiry},${u.status}`)].join("\\n");
      break;
    }
    case "payments": {
      var pdata=[]; try{pdata=JSON.parse(localStorage.getItem('ar_payments')||'[]');}catch{}
      csv = ["User,Plan,Amount,Reference,Time,Status",...pdata.map(p=>`${p.user},${p.plan},${p.amount},"${p.ref||''}",${p.time||''},${p.status||''}`)].join("\\n");
      break;
    }
    case "support": {
      var sdata=[]; try{sdata=JSON.parse(localStorage.getItem('ar_support_queries')||'[]');}catch{}
      csv = ["Name,Email,Subject,Status,Time",...sdata.map(q=>`${q.name},${q.email},${q.subject},${q.status},${q.time}`)].join("\\n");
      break;
    }
    default:
      csv = "No data";
  }
  downloadFile(`${type}_report.csv`, csv, "text/csv");
  showToast(`${type.charAt(0).toUpperCase()+type.slice(1)} report downloaded!`, "success");
}"""

if old_export in content:
    content = content.replace(old_export, new_export, 1)
    print("Fixed exportCSV!")
else:
    print("ERROR: Could not find exportCSV. Searching...")
    idx = content.find('function exportCSV')
    print(repr(content[idx:idx+400]))

with open('admin/admin.js', 'w', encoding='utf-8') as f:
    f.write(content)
print("Done!")
