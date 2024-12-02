/** @odoo-module */

import { Component, onWillStart, useRef, onMounted } from "@odoo/owl"
import { loadJS, loadCSS } from "@web/core/assets"

export class LeafletMapRenderer extends Component {
    static template = "leaflet_map.MapRenderer"
    static props = {}

    setup(){
        this.root = useRef('map')

        onWillStart(async ()=>{
            await loadCSS("https://unpkg.com/leaflet@1.9.4/dist/leaflet.css")
            await loadJS("https://unpkg.com/leaflet@1.9.4/dist/leaflet.js")
        })

        onMounted(()=>{
            this.map = L.map(this.root.el).setView([12.5687, 78.5749], 13);
           L.tileLayer('http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', {
              maxZoom: 20,
              subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
            }).addTo(this.map);


            const marker = L.marker([12.5687, 78.5749]).addTo(this.map);
            marker.bindPopup("<b>Hi!</b><br>Your in Jolarpet - 635851. <br/><br/>");
        })
    }
}
