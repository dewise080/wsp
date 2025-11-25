# Transfer Notes

## Files included
- templates/index-clean.html, hero-flow.html, modifier.html, playbooks-flow.html
- assets/styles.css, animations.css, flow.css, react-hero-flow.css, react-playbooks-flow.css, carousel.css
- assets/animations.js, carousel.js, react-hero-flow.js, landing-react-flow.js, react-playbooks-flow.js, react-appointments-flow.js, flow-modifier.js
- assets/flow-data.json plus landing-nodes.csv, landing-edges.csv, landing-items.csv
- assets/InterSemiBold-b0b540e6.ttf, MontserratBold-98b14868.ttf, MontserratSemiBold-e23dc6d2.ttf
- static/reactflow.css

## How the templates render
- index-clean.html loads CSS (styles/animations/flow + react flow skins + carousel) and JS (animations/carousel + four flow scripts) plus React/ReactDOM/@xyflow/react via importmap; it embeds hero, landing, playbooks, and appointments flows.
- modifier.html is the editing surface; it loads flow-modifier.js and react flow CSS to edit the JSON graph and export flow-data.json (or CSVs) for use by landing-react-flow.js.
- hero-flow.html and playbooks-flow.html are snippet-only embeds; they rely on the page to have already loaded the relevant CSS/JS.

## Workflow (JSON-driven)
- landing-react-flow.js fetches assets/flow-data.json (no-cache). If missing, it falls back to a hard-coded default. It builds nodes/edges, adjusts handles and edge anchors per layout (desktop vs mobile), and renders on #rf-canvas-landing.
- flow-data.json schema: nodes with id, type (eventNode|agentNode|connectorNode|actionNode|logicNode), label, description, iconSlug/iconColor/iconAlt, items[], posDesktop{x,y}, posMobile{x,y}; edges with id/source/target. Icons/items resolve via SimpleIcons CDN.
- flow-modifier.js lets you add/delete nodes, drag positions, edit metadata (type/label/description/icon/items), and switch desktop/mobile. "Save JSON" downloads the merged flow-data.json updating the current layout positions; "Save CSV" exports landing-nodes.csv, landing-edges.csv, landing-items.csv for spreadsheets. Replace assets/flow-data.json in your new project and reload the landing page to apply changes.

## Usage in a new project
- Serve the HTML from templates/, keeping asset paths or adjust href/src accordingly.
- Ensure the importmap/CDN for React + @xyflow/react CSS are available or replace with your bundler equivalents.
- Keep assets/flow-data.json reachable at the same relative path for landing-react-flow.js; run modifier.html to edit and re-export when needed.
