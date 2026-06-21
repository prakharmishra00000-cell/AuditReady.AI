"""Fix the corrupted section in admin.js where buildVisitorChart and buildUsersTable
got merged together due to bad replace_file_content operations."""

with open('admin/admin.js', 'r', encoding='utf-8') as f:
    content = f.read()

# The broken section is between buildVisitorChart ending and the paged section
# We need to insert the missing code between line 514 (lbl = ..) and "if (!paged"
bad_section = """    const lbl = document.createElement("span");

  if (!paged.length) {"""

fixed_section = """    const lbl = document.createElement("span");
    lbl.textContent = i % 5 === 0 ? `D${i+1}` :"";
    labels.appendChild(lbl);
  });
}

/* ******************************************************
   USERS TABLE
****************************************************** */
function buildUsersTable(filter ="", planFilter ="") {
  const tbody = document.getElementById("users-tbody");
  if (!tbody) return;
  // Read real users from localStorage (written by main site sign-up)
  let stored = []; try { stored = JSON.parse(localStorage.getItem('ar_accounts') || '[]'); } catch {}
  // Enrich with plan data
  let users = stored.map(function(u) {
    var planRaw = null; try { planRaw = JSON.parse(localStorage.getItem('ar_plan_' + u.email.toLowerCase()) || 'null'); } catch {}
    return { name: u.name || u.email.split('@')[0], email: u.email, plan: planRaw ? planRaw.plan : 'free',
             joined: u.created ? new Date(u.created).toLocaleDateString('en-IN') : '--',
             expiry: planRaw && planRaw.expiry ? new Date(planRaw.expiry).toLocaleDateString('en-IN') : '--',
             status: u.suspended ? 'suspended' : (planRaw && Date.now() < planRaw.expiry ? 'active' : (planRaw ? 'expired' : 'free')), id: u.email };
  });
  if (filter)     users = users.filter(u => u.name.toLowerCase().includes(filter) || u.email.toLowerCase().includes(filter));
  if (planFilter) users = users.filter(u => u.plan === planFilter.toLowerCase());

  const pages  = Math.ceil(users.length / PAGE_SIZE);
  const paged  = users.slice((currentPage-1)*PAGE_SIZE, currentPage*PAGE_SIZE);

  document.getElementById("page-indicator").textContent = `Page ${currentPage} of ${pages || 1}`;
  document.getElementById("prev-page-btn").disabled = currentPage <= 1;
  document.getElementById("next-page-btn").disabled = currentPage >= pages;

  if (!paged.length) {"""

if bad_section in content:
    content = content.replace(bad_section, fixed_section, 1)
    print("Fixed the corrupted section!")
else:
    print("ERROR: Could not find the corrupted section. Checking what's there...")
    idx = content.find('const lbl = document.createElement("span");')
    print(repr(content[idx:idx+200]))

with open('admin/admin.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done!")
