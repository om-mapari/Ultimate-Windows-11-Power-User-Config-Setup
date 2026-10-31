// ==UserScript==
// @name         Jellyfin - hide player controls
// @namespace    http://www.xyz.net/
// @version      0.3
// @description  Add shortcut in Jellyfin video player for hiding/showing all controls and overlays (press 'g' to toggle).
// @author       CoderOm
// @match        http://jellyfin.local:8096/web/*
// @match        http://localhost:8096/web/*
// @include      /^http:\/\/[^\/]*?:8096\/web\/.*?$/
// @run-at       document-idle
// @grant        none
// ==/UserScript==

(function () {
    "use strict";

    const style = document.createElement("style");
    style.id = "jf-hide-controls-style";
    style.textContent = `
        .jf-hide-controls .skinHeader,
        .jf-hide-controls .osdHeader,
        .jf-hide-controls #videoOsdPage,
        .jf-hide-controls .videoOsdBottom,
        .jf-hide-controls .osdControls,
        .jf-hide-controls #pause-screen-overlay,
        .jf-hide-controls .upNextContainer,
        .jf-hide-controls .jfQueuePanel,
        .jf-hide-controls .appfooter,
        .jf-hide-controls .docspinner,
        .jf-hide-controls .subtitleSync {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
        }
    `;
    document.head.appendChild(style);

    document.addEventListener("keydown", function (e) {
        if (e.target && e.target.tagName && ["INPUT", "TEXTAREA", "SELECT"].includes(e.target.tagName)) return;
        if (e.target && e.target.isContentEditable) return;

        if (e.key && e.key.toLowerCase() === "g") {
            document.body.classList.toggle("jf-hide-controls");
        }
    });
})();
