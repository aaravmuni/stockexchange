// sectionhandler.js — section navigation + GA4 analytics

let sections = [];

// ---- analytics state ----
let currentSection = null; // the section currently shown
let sectionStart = null;   // ms timestamp when currentSection became visible

// Report the time spent on the section we're about to leave, then reset the
// clock. Attributed to currentSection — the one we were actually viewing.
function flushTimeSpent() {
  if (currentSection === null || sectionStart === null) return;
  const seconds = Math.round((Date.now() - sectionStart) / 1000);
  sectionStart = Date.now(); // reset now so a span is never counted twice
  if (seconds <= 0) return;  // skip instant flips
  gtag("event", "time_on_section", {
    section_name: currentSection,
    time_seconds: seconds,
  });
}

document.querySelectorAll(".sectionselect").forEach(link => {
  sections.push(link.dataset.section);
  link.addEventListener("click", (e) => {
    e.preventDefault();
    switchtosection(link.dataset.section);
  });
});

window.addEventListener("hashchange", () => {
  const section = window.location.hash.slice(1);
  if (section) switchtosection(section);
});

window.addEventListener("DOMContentLoaded", () => {
  const section = window.location.hash.slice(1);
  switchtosection(section || "explore");
});

// Tab hidden or being closed: bank the current section's time NOW.
// gtag sends via navigator.sendBeacon, so this survives the page tearing
// down — a request fired on `unload` usually would not.
document.addEventListener("visibilitychange", () => {
  if (document.visibilityState === "hidden") {
    flushTimeSpent();
  } else {
    sectionStart = Date.now(); // back in focus — resume the clock
  }
});

switchtosection("explore");

function switchtosection(sec) {
  if (!sections.includes(sec)) {
    console.log("no section exists named: " + sec);
    switchtosection("explore");
    return;
  }

  sections.forEach(section => {
    const s = document.querySelector("#" + section);
    if (section === sec) {
      s.style.display = "block";
      window.location.hash = sec;
    } else {
      s.style.display = "none";
    }
  });

  // Only fire analytics on a REAL change. A click sets the hash, which fires
  // `hashchange`, which calls this again with the same value — this guard
  // makes that repeat a no-op, so every switch is counted exactly once.
  if (sec !== currentSection) {
    flushTimeSpent();                                        // close out the old section
    gtag("event", "section_change", { section_name: sec });  // record the new one
    currentSection = sec;
    sectionStart = Date.now();                               // start timing the new section
  }
}