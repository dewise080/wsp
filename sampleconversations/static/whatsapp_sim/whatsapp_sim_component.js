(() => {
    const run = () => {
        const Constructor = window.WhatsappSim ? window.WhatsappSim.constructor : null;
        const createInstance = () => {
            if (Constructor) {
                return new Constructor();
            }
            return window.WhatsappSim || null;
        };

        document.querySelectorAll("[data-wsim]").forEach((node) => {
            const sampleId = node.dataset.wsimSampleId;
            const sampleEl = sampleId ? document.getElementById(sampleId) : null;
            const output = node.querySelector("[data-wsim-output]");
            const status = node.querySelector("[data-wsim-status]");

            if (!sampleEl || !output) {
                return;
            }

            let sampleText = "";
            try {
                sampleText = JSON.parse(sampleEl.textContent || "\"\"");
            } catch (err) {
                sampleText = sampleEl.textContent || "";
            }

            const sim = createInstance();
            if (!sim || typeof sim.parse !== "function") {
                if (status) {
                    status.textContent = "Simulator library not available.";
                }
                return;
            }

            output.innerHTML = "";
            if (status) {
                status.textContent = "Replaying chat…";
            }

            sim.onMessage = (msg) => {
                output.appendChild(sim.createMsgElement(msg));
                output.scrollTop = output.scrollHeight;
            };

            sim.onComplete = () => {
                if (status) {
                    status.textContent = "Replay complete.";
                }
            };

            sim.parse(sampleText);

            const primary = node.dataset.wsimPrimary;
            if (primary) {
                sim.setPrimaryAuthor(primary);
            }

            const replayType = node.dataset.wsimReplayType || "word";
            sim.config({ replayType });

            sim.startSimulation();
        });
    };

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", run);
    } else {
        run();
    }
})();
