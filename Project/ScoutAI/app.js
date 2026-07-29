const API = window.location.origin.startsWith("http") ? window.location.origin : "http://127.0.0.1:8000";

let skillChart = null;
let matchChart = null;
let currentJobs = [];
let currentResumeId = localStorage.getItem("smartscout_resume_id") ? parseInt(localStorage.getItem("smartscout_resume_id")) : null;
let activeModalJob = null;

// HTML Escaper
function escapeHtml(value) {
    if (value === null || value === undefined) return "";
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#39;");
}

// Tab Switching System
document.querySelectorAll(".nav-item").forEach(button => {
    button.addEventListener("click", () => {
        const targetTab = button.dataset.tab;

        document.querySelectorAll(".nav-item").forEach(b => b.classList.remove("active"));
        document.querySelectorAll(".tab-content").forEach(t => t.classList.remove("active"));

        button.classList.add("active");
        document.getElementById(`tab-${targetTab}`).classList.add("active");

        // Update titles
        const titleMap = {
            dashboard: { title: "Dashboard Overview", sub: "AI-powered market insights and candidate job fit metrics" },
            explorer: { title: "Job Explorer", sub: "Browse, filter, and inspect detailed software engineering postings" },
            resume: { title: "Resume & AI Profile", sub: "Upload your resume to calculate personalized match scores" },
            roadmap: { title: "Skill Gap Learning Roadmap", sub: "Actionable weekly learning paths derived from targeted job requirements" }
        };

        if (titleMap[targetTab]) {
            document.getElementById("page-title").innerText = titleMap[targetTab].title;
            document.getElementById("page-subtitle").innerText = titleMap[targetTab].sub;
        }

        if (window.lucide) window.lucide.createIcons();
    });
});

// Event Listeners
document.getElementById("search-btn").addEventListener("click", searchJobs);
document.getElementById("upload-btn").addEventListener("click", uploadResume);
document.getElementById("generate-roadmap-btn").addEventListener("click", generateRoadmap);
document.getElementById("analyse-all-btn").addEventListener("click", reanalyseJobs);

// File Drop Zone
const dropZone = document.getElementById("drop-zone");
const fileInput = document.getElementById("resume");

dropZone.addEventListener("click", (e) => {
    if (e.target !== fileInput) {
        fileInput.click();
    }
});

["dragenter", "dragover"].forEach(eventName => {
    dropZone.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropZone.classList.add("dragover");
    }, false);
});

["dragleave", "drop"].forEach(eventName => {
    dropZone.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropZone.classList.remove("dragover");
    }, false);
});

dropZone.addEventListener("drop", (e) => {
    const dt = e.dataTransfer;
    if (dt && dt.files && dt.files.length > 0) {
        fileInput.files = dt.files;
        dropZone.querySelector("h4").innerText = `Selected: ${dt.files[0].name}`;
    }
});

fileInput.addEventListener("change", () => {
    if (fileInput.files.length > 0) {
        dropZone.querySelector("h4").innerText = `Selected: ${fileInput.files[0].name}`;
    }
});

// Search Jobs
async function searchJobs() {
    const role = document.getElementById("role").value.trim();
    const location = document.getElementById("location").value.trim();

    if (!role) {
        alert("Please enter a job role.");
        return;
    }

    const searchBtn = document.getElementById("search-btn");
    searchBtn.disabled = true;
    searchBtn.innerHTML = `<i data-lucide="loader-2" class="spin"></i> Searching...`;
    if (window.lucide) window.lucide.createIcons();

    try {
        const response = await fetch(`${API}/search_jobs`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                role,
                location,
                resume_id: currentResumeId
            })
        });

        const data = await response.json();
        currentJobs = data.jobs || [];

        updateDashboard(data.dashboard);
        renderTableJobs(currentJobs);
        renderExplorerCards(currentJobs);

    } catch (err) {
        console.error(err);
        alert("Failed to search jobs. Please ensure the backend server is running.");
    } finally {
        searchBtn.disabled = false;
        searchBtn.innerHTML = `<i data-lucide="sparkles"></i> <span>Search Jobs</span>`;
        if (window.lucide) window.lucide.createIcons();
    }
}

// Upload Resume
async function uploadResume() {
    const file = fileInput.files[0];
    if (!file) {
        alert("Please select a resume file (PDF, DOCX, or TXT) first.");
        return;
    }

    const uploadBtn = document.getElementById("upload-btn");
    uploadBtn.disabled = true;
    uploadBtn.innerHTML = `<i data-lucide="loader-2" class="spin"></i> Parsing Resume...`;
    if (window.lucide) window.lucide.createIcons();

    const form = new FormData();
    form.append("resume", file);
    form.append("file", file);

    try {
        const response = await fetch(`${API}/upload_resume`, {
            method: "POST",
            body: form
        });

        const data = await response.json();

        if (response.ok && data.success) {
            currentResumeId = data.resume_id;
            localStorage.setItem("smartscout_resume_id", currentResumeId);

            renderParsedResume(data.resume);
            document.getElementById("sidebar-resume-badge").style.borderColor = "var(--emerald)";
            document.getElementById("active-resume-name").innerText = data.resume.name || file.name;
            document.getElementById("analyse-all-btn").style.display = "inline-flex";

            alert("Resume parsed and saved successfully!");
            reanalyseJobs();
        } else {
            alert(data.detail || data.message || "Resume upload failed.");
        }
    } catch (err) {
        console.error("Upload error:", err);
        alert("Error uploading resume: " + err.message);
    } finally {
        uploadBtn.disabled = false;
        uploadBtn.innerHTML = `<i data-lucide="cpu"></i> <span>Upload & Parse Resume</span>`;
        if (window.lucide) window.lucide.createIcons();
    }
}

// Re-analyse Current Jobs with Resume
async function reanalyseJobs() {
    if (!currentResumeId) {
        alert("Upload a resume first.");
        return;
    }

    try {
        const response = await fetch(`${API}/jobs/analyse`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ resume_id: currentResumeId })
        });

        if (response.ok) {
            const data = await response.json();
            currentJobs = data.results || [];
            
            // Reload dashboard metrics
            loadDashboardMetrics();
            renderTableJobs(currentJobs);
            renderExplorerCards(currentJobs);
        }
    } catch (err) {
        console.error("Re-analysis failed:", err);
    }
}

// Render Parsed Resume Details
function renderParsedResume(resume) {
    const container = document.getElementById("resume-details-container");
    if (!resume) return;

    let skillsHtml = (resume.skills || []).map(s => `<span class="tag">${escapeHtml(s)}</span>`).join(" ");

    container.innerHTML = `
        <div class="resume-field-group">
            <h5>Candidate Name</h5>
            <h3>${escapeHtml(resume.name || "Unknown")}</h3>
        </div>
        <div class="resume-field-group">
            <h5>Contact</h5>
            <p>${escapeHtml(resume.email || "")} ${resume.phone ? "• " + escapeHtml(resume.phone) : ""}</p>
        </div>
        <div class="resume-field-group">
            <h5>Extracted Skills</h5>
            <div class="tag-cloud">${skillsHtml || "<span class='text-muted'>None detected</span>"}</div>
        </div>
        <div class="resume-field-group">
            <h5>Professional Summary</h5>
            <p class="text-muted">${escapeHtml(resume.summary || "N/A")}</p>
        </div>
    `;
}

// Dashboard Update
function updateDashboard(data) {
    if (!data) return;

    const overview = data.overview || {};
    document.getElementById("total-jobs").innerText = overview.total_jobs || 0;
    document.getElementById("avg-match").innerText = (overview.average_match || 0) + "%";
    document.getElementById("priority").innerText = overview.high_priority || 0;
    document.getElementById("companies").innerText = overview.companies || 0;

    drawSkillChart(data.top_skills);
    drawMatchChart(data.match_distribution);
}

// Load Dashboard Metrics Endpoint
async function loadDashboardMetrics() {
    try {
        const url = `${API}/dashboard${currentResumeId ? '?resume_id=' + currentResumeId : ''}`;
        const response = await fetch(url);
        if (response.ok) {
            const data = await response.json();
            updateDashboard(data);
        }
    } catch (err) {
        console.error("Dashboard fetch error:", err);
    }
}

// Render Jobs Table in Dashboard
function renderTableJobs(jobs) {
    const table = document.getElementById("job-table");
    table.innerHTML = "";

    document.getElementById("result-count-badge").innerText = `${jobs.length} Results`;

    if (!jobs || jobs.length === 0) {
        table.innerHTML = `
            <tr>
                <td colspan="6" class="empty-state">
                    <i data-lucide="search-x"></i>
                    <p>No jobs found. Enter a role above and search.</p>
                </td>
            </tr>
        `;
        if (window.lucide) window.lucide.createIcons();
        return;
    }

    jobs.forEach((item, index) => {
        const info = item.job || item;
        const analysis = item.analysis || {
            overall_score: item.match_score || 75,
            priority: "Medium",
            strengths: item.required_skills || [],
            missing_skills: item.missing_skills || []
        };

        const score = analysis.overall_score || 0;
        const scoreBadgeClass = score >= 85 ? "badge-emerald" : (score >= 65 ? "badge-blue" : "badge-amber");

        const row = document.createElement("tr");
        row.innerHTML = `
            <td><strong>${escapeHtml(info.title)}</strong></td>
            <td>${escapeHtml(info.company)}</td>
            <td>${escapeHtml(info.location)}</td>
            <td><span class="badge ${scoreBadgeClass}">${score}% Match</span></td>
            <td><span class="badge badge-accent">${escapeHtml(analysis.priority || "Normal")}</span></td>
            <td>
                <button data-job-index="${index}" class="btn btn-primary btn-sm view-btn">
                    <i data-lucide="eye"></i> View Details
                </button>
            </td>
        `;
        table.appendChild(row);
    });

    if (window.lucide) window.lucide.createIcons();
}

// Render Job Explorer Cards Grid
function renderExplorerCards(jobs) {
    const grid = document.getElementById("explorer-jobs-grid");
    grid.innerHTML = "";

    if (!jobs || jobs.length === 0) {
        grid.innerHTML = `<div class="empty-state" style="grid-column: 1/-1;"><i data-lucide="search"></i><p>No matching jobs to display.</p></div>`;
        if (window.lucide) window.lucide.createIcons();
        return;
    }

    const minScore = parseInt(document.getElementById("score-filter").value) || 0;
    const remoteOnly = document.getElementById("remote-filter").checked;
    const keyword = document.getElementById("keyword-filter").value.toLowerCase();

    let filtered = jobs.filter(item => {
        const info = item.job || item;
        const analysis = item.analysis || {};
        const score = analysis.overall_score || info.match_score || 70;

        if (score < minScore) return false;
        if (remoteOnly && !info.remote) return false;
        if (keyword) {
            const haystack = `${info.title} ${info.company} ${info.location} ${(info.required_skills||[]).join(" ")}`.toLowerCase();
            if (!haystack.includes(keyword)) return false;
        }
        return true;
    });

    if (filtered.length === 0) {
        grid.innerHTML = `<div class="empty-state" style="grid-column: 1/-1;"><p>No jobs match current filter options.</p></div>`;
        return;
    }

    filtered.forEach((item, index) => {
        const info = item.job || item;
        const analysis = item.analysis || {};
        const score = analysis.overall_score || 75;
        const originalIndex = jobs.indexOf(item);

        const card = document.createElement("div");
        card.className = "job-card";
        card.innerHTML = `
            <div class="job-card-header">
                <div>
                    <h3 class="job-card-title">${escapeHtml(info.title)}</h3>
                    <span class="job-card-company">${escapeHtml(info.company)} • ${escapeHtml(info.location)}</span>
                </div>
                <span class="badge ${score >= 80 ? 'badge-emerald' : 'badge-blue'}">${score}%</span>
            </div>
            <div class="tag-cloud">
                ${(info.required_skills || []).slice(0, 4).map(s => `<span class="tag">${escapeHtml(s)}</span>`).join("")}
            </div>
            <button data-job-index="${originalIndex}" class="btn btn-primary btn-block btn-sm view-btn">
                View Opportunity
            </button>
        `;
        grid.appendChild(card);
    });
}

// Explorer Filters Listeners
document.getElementById("score-filter").addEventListener("input", (e) => {
    document.getElementById("score-val").innerText = `${e.target.value}%`;
    renderExplorerCards(currentJobs);
});
document.getElementById("remote-filter").addEventListener("change", () => renderExplorerCards(currentJobs));
document.getElementById("keyword-filter").addEventListener("input", () => renderExplorerCards(currentJobs));

// Table/Grid View Click Delegation
document.addEventListener("click", (event) => {
    const btn = event.target.closest(".view-btn");
    if (btn && btn.dataset.jobIndex !== undefined) {
        const index = parseInt(btn.dataset.jobIndex);
        if (currentJobs[index]) {
            openJobModal(currentJobs[index]);
        }
    }
});

// Modal Logic
function openJobModal(item) {
    activeModalJob = item;
    const info = item.job || item;
    const analysis = item.analysis || {};

    const score = analysis.overall_score || info.match_score || 75;
    document.getElementById("modal-score").innerText = `${score}% Match Fit`;
    document.getElementById("modal-priority").innerText = `Priority: ${analysis.priority || 'High'}`;
    document.getElementById("modal-title").innerText = info.title || "Job Details";
    document.getElementById("modal-company").innerHTML = `<i data-lucide="building"></i> ${escapeHtml(info.company)}`;
    document.getElementById("modal-location").innerHTML = `<i data-lucide="map-pin"></i> ${escapeHtml(info.location)}`;
    document.getElementById("modal-salary").innerHTML = `<i data-lucide="dollar-sign"></i> ${escapeHtml(info.salary || "Competitive Market Rate")}`;

    document.getElementById("modal-explanation").innerText = analysis.explanation || "Analyzed based on skill overlap and required qualifications.";

    const strengths = analysis.strengths || info.required_skills || [];
    document.getElementById("modal-strengths").innerHTML = strengths.map(s => `<span class="badge badge-emerald">${escapeHtml(s)}</span>`).join(" ") || "<span class='text-muted'>None specified</span>";

    const missing = analysis.missing_skills || [];
    document.getElementById("modal-missing").innerHTML = missing.map(s => `<span class="badge badge-amber">${escapeHtml(s)}</span>`).join(" ") || "<span class='badge badge-emerald'>No Skill Gaps Detected!</span>";

    document.getElementById("modal-description").innerText = info.job_description || "No full description provided.";

    document.getElementById("modal-interview-questions").innerHTML = `<span class="text-muted">Click "Predict Questions" to generate targeted interview questions for this position.</span>`;
    document.getElementById("modal-apply-btn").href = info.application_url || "https://www.linkedin.com/jobs";

    document.getElementById("job-modal").classList.add("active");
    if (window.lucide) window.lucide.createIcons();
}

document.getElementById("modal-close-btn").addEventListener("click", () => {
    document.getElementById("job-modal").classList.remove("active");
});

// Predict Interview Questions in Modal
document.getElementById("generate-questions-btn").addEventListener("click", async () => {
    if (!activeModalJob) return;

    const btn = document.getElementById("generate-questions-btn");
    const container = document.getElementById("modal-interview-questions");
    btn.disabled = true;
    btn.innerText = "Predicting...";

    try {
        const response = await fetch(`${API}/jobs/interview-questions`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                resume_id: currentResumeId,
                job: activeModalJob.job || activeModalJob
            })
        });

        const data = await response.json();
        let html = "";

        if (data.technical && data.technical.length > 0) {
            html += `<strong>Technical Questions:</strong><ul class="interview-list">`;
            data.technical.forEach(q => html += `<li>${escapeHtml(q)}</li>`);
            html += `</ul>`;
        }

        if (data.behavioural && data.behavioural.length > 0) {
            html += `<strong style="margin-top:10px; display:block;">Behavioral Questions:</strong><ul class="interview-list">`;
            data.behavioural.forEach(q => html += `<li>${escapeHtml(q)}</li>`);
            html += `</ul>`;
        }

        container.innerHTML = html || "<p>Interview questions generated cleanly.</p>";

    } catch (err) {
        console.error(err);
        container.innerHTML = `<span class="text-amber">Failed to predict interview questions.</span>`;
    } finally {
        btn.disabled = false;
        btn.innerHTML = `<i data-lucide="help-circle"></i> Predict Questions`;
        if (window.lucide) window.lucide.createIcons();
    }
});

// Generate Learning Roadmap
async function generateRoadmap() {
    if (!currentResumeId) {
        alert("Please upload your resume in the 'Resume & AI Match' tab first.");
        return;
    }

    const btn = document.getElementById("generate-roadmap-btn");
    const output = document.getElementById("roadmap-output");

    btn.disabled = true;
    btn.innerHTML = `<i data-lucide="loader-2" class="spin"></i> Generating...`;
    if (window.lucide) window.lucide.createIcons();

    try {
        const response = await fetch(`${API}/learning-plan`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ resume_id: currentResumeId })
        });

        const data = await response.json();
        const plan = data.learning_plan;

        if (plan && plan.weeks && plan.weeks.length > 0) {
            let html = `<div class="timeline">`;
            plan.weeks.forEach(w => {
                html += `
                    <div class="timeline-item">
                        <h4>Week ${w.week}: ${escapeHtml(w.goal || "Skill Mastery")}</h4>
                        <p class="text-muted">Key Topics: ${(w.topics || []).map(t => escapeHtml(t)).join(", ")}</p>
                    </div>
                `;
            });
            html += `</div>`;
            if (plan.final_goal) {
                html += `<div style="margin-top:20px;" class="badge badge-emerald">Final Target: ${escapeHtml(plan.final_goal)}</div>`;
            }
            output.innerHTML = html;
        } else {
            output.innerHTML = `<div class="empty-state"><p>${escapeHtml(plan.summary || "No major skill gaps identified for your target roles!")}</p></div>`;
        }

    } catch (err) {
        console.error(err);
        alert("Failed to generate learning roadmap.");
    } finally {
        btn.disabled = false;
        btn.innerHTML = `<i data-lucide="sparkles"></i> <span>Generate Roadmap</span>`;
        if (window.lucide) window.lucide.createIcons();
    }
}

// Chart.js Drawing Helpers
function drawSkillChart(data) {
    if (!data) return;
    const ctx = document.getElementById("skillChart");
    if (!ctx) return;

    if (skillChart) skillChart.destroy();

    const labels = Object.keys(data).slice(0, 8);
    const values = Object.values(data).slice(0, 8);

    skillChart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                label: "Required Jobs",
                data: values,
                backgroundColor: "rgba(99, 102, 241, 0.6)",
                borderColor: "#6366f1",
                borderWidth: 1,
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                x: { ticks: { color: "#94a3b8" }, grid: { display: false } },
                y: { ticks: { color: "#94a3b8" }, grid: { color: "rgba(255,255,255,0.05)" } }
            }
        }
    });
}

function drawMatchChart(data) {
    if (!data) return;
    const ctx = document.getElementById("matchChart");
    if (!ctx) return;

    if (matchChart) matchChart.destroy();

    matchChart = new Chart(ctx, {
        type: "doughnut",
        data: {
            labels: Object.keys(data),
            datasets: [{
                data: Object.values(data),
                backgroundColor: ["#10b981", "#6366f1", "#f59e0b", "#a855f7", "#ef4444"],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: "right", labels: { color: "#94a3b8", font: { size: 11 } } }
            }
        }
    });
}

// Initial Page Load
window.onload = function () {
    if (currentResumeId) {
        document.getElementById("sidebar-resume-badge").style.borderColor = "var(--emerald)";
        document.getElementById("active-resume-name").innerText = `Resume ID #${currentResumeId}`;
        document.getElementById("analyse-all-btn").style.display = "inline-flex";
    }

    searchJobs();
};