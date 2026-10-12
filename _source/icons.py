# Veeyes icon set: original 24px line icons, navy stroke (currentColor) with one cyan accent (var(--accent)).
# Drawn for this site; the tooth outline is shared so the set reads as one family.

TOOTH = ("M7.6 3.2C5.3 3.2 4 5 4 7.3c0 2 .7 3.3 1.2 4.7.6 1.7.7 3.5 1 5.5.3 2 .9 3.3 1.9 3.3 1.3 0 1.5-1.7 1.9-3.7"
         ".3-1.5.8-2.5 2-2.5s1.7 1 2 2.5c.4 2 .6 3.7 1.9 3.7 1 0 1.6-1.3 1.9-3.3.3-2 .4-3.8 1-5.5.5-1.4 1.2-2.7 1.2-4.7"
         " 0-2.3-1.3-4.1-3.6-4.1-1.8 0-2.6 1-4.4 1s-2.6-1-4.4-1Z")
A = 'fill="var(--accent,#12c2d2)" stroke="none"'          # solid accent
AS = 'stroke="var(--accent,#12c2d2)"'                      # accent stroke
def tooth(t=""): return f'<path d="{TOOTH}"{f" transform=\"{t}\"" if t else ""}/>'

def _arch():
    import math
    s = '<path d="M4 15c0-5.6 3.6-10 8-10s8 4.4 8 10"/><path d="M7.5 15c0-3.8 2-6.8 4.5-6.8s4.5 3 4.5 6.8"/>'
    for deg in (150, 120, 90, 60, 30):
        r = math.radians(deg)
        x1, y1 = 12 + 8 * math.cos(r), 15 - 10 * math.sin(r)
        x2, y2 = 12 + 4.5 * math.cos(r), 15 - 6.8 * math.sin(r)
        s += f'<path d="M{x1:.1f} {y1:.1f}L{x2:.1f} {y2:.1f}"/>'
    return s + f'<path d="M3 19h18" {AS} stroke-width="2"/>'

ICONS = {
 "tooth": tooth() + f'<path d="M7.2 6.6c.3-.9 1-1.4 1.9-1.4" {AS}/>',
 "braces": tooth() + f'<path d="M2.5 9.5h19"/><rect x="6.6" y="8" width="3" height="3" rx=".6" {A}/><rect x="14.4" y="8" width="3" height="3" rx=".6" {A}/>',
 "aligner": f'<path d="{TOOTH}" {AS} stroke-width="1.4"/>' + tooth("translate(3.36 3) scale(.72)"),
 "implant": f'<path d="M7 3.5h10c1.4 0 2.3 1.2 2 2.6l-.9 3.4H5.9L5 6.1C4.7 4.7 5.6 3.5 7 3.5Z"/><path d="M10.2 9.5h3.6V12h-3.6z"/><path d="M9 12h6l-1 9.5h-4z"/><path d="M8.9 14.4h6.2M9.2 16.8h5.6M9.5 19.2h5" {AS}/>',
 "hour": tooth("translate(0 .5) scale(.8)") + f'<circle cx="17.3" cy="17.3" r="5.2" {A}/><path d="M17.3 14.6v2.9l1.9 1.2" stroke="#fff"/>',
 "arch": _arch(),
 "filling": tooth() + f'<path d="M8.6 7.3c1.1.6 2.3.9 3.4.9s2.3-.3 3.4-.9l.5 2.6c-1.3.7-2.6 1.1-3.9 1.1s-2.6-.4-3.9-1.1z" {A}/>',
 "leaf": tooth("translate(0 2.6) scale(.82)") + f'<path d="M14.2 9.6c0-4 2.8-7 7-7 0 4-2.8 7-7 7Z" {A}/><path d="M14.4 9.4l3.6-3.6" stroke="#fff" stroke-width="1.2"/>',
 "crack": tooth() + f'<path d="M12.9 4.4l-1.8 3 2.2 1.8-2 3.4" {AS} stroke-width="1.8"/>',
 "sparkle": tooth("translate(0 3.4) scale(.8)") + f'<path d="M18.6 1.6l.9 2.2 2.2.9-2.2.9-.9 2.2-.9-2.2-2.2-.9 2.2-.9z" {A}/><path d="M21.3 9.2l.4 1 1 .4-1 .4-.4 1-.4-1-1-.4 1-.4z" {A}/>',
 "smile": f'<path d="M12 3v18" {AS} stroke-dasharray="1.5 2"/><path d="M3.5 9.5c2.6.9 5.4 1.3 8.5 1.3s5.9-.4 8.5-1.3"/><path d="M3.5 9.5c2.2 4.8 5.1 7 8.5 7s6.3-2.2 8.5-7"/><path d="M8.2 11v3.6M15.8 11v3.6"/>',
 "shine": tooth("translate(2.6 4.6) scale(.78)") + f'<path d="M12 1.2v2.3M5.4 2.9l1.4 1.6M18.6 2.9l-1.4 1.6M2.2 7.6l1.9.5M21.8 7.6l-1.9.5" {AS}/>',
 "laser": tooth("translate(4.6 4.4) scale(.8)") + f'<path d="M2.6 5.4l2.8-2.8 3.4 3.4L6 8.8z"/><path d="M8 8l4.2 4.2" {AS} stroke-width="2"/><circle cx="13.2" cy="13.2" r="1.3" {A}/>',
 "canal": tooth() + f'<path d="M9.4 8.6c1.7.9 3.5.9 5.2 0M10 9.4c.4 2.6.4 5.2.1 7.8M14 9.4c-.4 2.6-.4 5.2-.1 7.8" {AS}/>',
 "shield": f'<path d="M12 2.8l7.2 2.9v5.8c0 4.7-3.1 8.1-7.2 9.7-4.1-1.6-7.2-5-7.2-9.7V5.7z"/>' + f'<path d="{TOOTH}" transform="translate(7.1 6.6) scale(.41)" {A}/>',
 "kid": tooth() + '<circle cx="9.6" cy="8.4" r=".9" fill="currentColor" stroke="none"/><circle cx="14.4" cy="8.4" r=".9" fill="currentColor" stroke="none"/>' + f'<path d="M10 11c1.2 1 2.8 1 4 0" {AS} stroke-width="1.8"/>',
 "care": tooth("translate(0 .4) scale(.8)") + f'<path d="M17.4 22s-4.6-2.7-4.6-5.8a2.4 2.4 0 0 1 4.6-1 2.4 2.4 0 0 1 4.6 1c0 3.1-4.6 5.8-4.6 5.8Z" {A}/>',
 "gum": tooth() + f'<path d="M2.5 13c1.6-1.1 3.2-1.1 4.8 0s3.2 1.1 4.7 0 3.2-1.1 4.7 0 3.2 1.1 4.8 0" {AS} stroke-width="2"/>',
 "screen": '<rect x="2.8" y="3.8" width="18.4" height="12.4" rx="2"/><path d="M9 20.2h6M12 16.2v4"/>' + f'<path d="{TOOTH}" transform="translate(8.3 5.4) scale(.31)" {A}/>',
 "xray": '<rect x="4" y="2.8" width="16" height="18.4" rx="2.2"/>' + f'<path d="{TOOTH}" transform="translate(5.6 6) scale(.53)" {AS}/><path d="M7 5.6h2" {AS}/>',
 # why-veeyes + facilities
 "badge": f'<circle cx="12" cy="9.2" r="5.8"/><path d="M8.6 13.8 7.2 21.2l4.8-2.4 4.8 2.4-1.4-7.4"/><path d="M9.6 9.2l1.7 1.7 3.2-3.3" {AS} stroke-width="1.8"/>',
 "grid": f'<rect x="3.5" y="3.5" width="7" height="7" rx="1.8"/><rect x="13.5" y="3.5" width="7" height="7" rx="1.8" {A}/><rect x="3.5" y="13.5" width="7" height="7" rx="1.8"/><rect x="13.5" y="13.5" width="7" height="7" rx="1.8"/>',
 "lamp": f'<path d="M4 21.2V10a3.2 3.2 0 0 1 3.2-3.2h4.6"/><path d="M2.5 21.2h6"/><path d="M11.8 4h8.6l-1.8 5h-5z"/><path d="M14 11.4l-.8 1.6M16.2 11.6v1.8M18.4 11.4l.8 1.6" {AS}/>',
 "talk": f'<path d="M4.3 4.5h10.4a1.8 1.8 0 0 1 1.8 1.8v5.6a1.8 1.8 0 0 1-1.8 1.8H9.4l-3.6 3v-3H4.3a1.8 1.8 0 0 1-1.8-1.8V6.3a1.8 1.8 0 0 1 1.8-1.8Z"/><path d="M18.6 9.2h.9a2 2 0 0 1 2 2v4.4a2 2 0 0 1-2 2h-.5v2.6l-3.1-2.6h-3.6" {AS}/>',
 "sterile": f'<path d="M12 2.8l7.2 2.9v5.8c0 4.7-3.1 8.1-7.2 9.7-4.1-1.6-7.2-5-7.2-9.7V5.7z"/><path d="M8.6 11.8l2.4 2.4 4.4-4.6" {AS} stroke-width="1.9"/>',
 "surgical": f'<circle cx="12" cy="11" r="7"/><path d="M12 4V1.8"/><circle cx="12" cy="8.4" r="1.4" {A}/><circle cx="9.3" cy="12.6" r="1.4" {A}/><circle cx="14.7" cy="12.6" r="1.4" {A}/><path d="M9 21h6"/>',
 "pulse": f'<rect x="2.8" y="4" width="18.4" height="13" rx="2"/><path d="M5.5 11h3l1.6-3.2 2.6 6 1.6-2.8h4.2" {AS} stroke-width="1.8"/><path d="M9 20.4h6"/>',
 "mask": f'<path d="M5.8 8.6h12.4l-1.5 6.8a3.2 3.2 0 0 1-3.1 2.5h-3.2a3.2 3.2 0 0 1-3.1-2.5z"/><path d="M5.8 8.6 3 6.8M18.2 8.6 21 6.8M12 17.9v3.3"/><path d="M9.2 12h5.6" {AS} stroke-width="1.8"/>',
 "pin": '<path d="M12 21.2s-6.8-6-6.8-10.8a6.8 6.8 0 0 1 13.6 0c0 4.8-6.8 10.8-6.8 10.8Z"/>' + f'<circle cx="12" cy="10.2" r="2.4" {A}/>',
}

def sprite():
    sym = "".join(
        f'<symbol id="ic-{k}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{v}</symbol>'
        for k, v in ICONS.items())
    return f'<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">{sym}</svg>'

def ic(name, cls="ic"):
    return f'<svg class="{cls}" aria-hidden="true" focusable="false"><use href="#ic-{name}"/></svg>'

# which icon goes where
TX_ICON = {
 "teeth-alignment": "braces", "invisalign": "aligner", "teeth-replacement": "implant", "teeth-in-an-hour": "hour",
 "full-mouth-rehabilitation": "arch", "restorative-dentistry": "filling", "biominmetic-dentistry": "leaf",
 "tooth-fracture-management": "crack", "cosmetic-dentistry": "sparkle", "smile-designing": "smile", "teeth-whitening": "shine",
 "laser-dentistry": "laser", "teeth-management": "canal", "preventive-dentistry": "shield", "kids-family-dentistry": "kid",
 "geriatric-dentistry": "care", "gum-treatment": "gum", "digital-dentistry": "screen", "digital-radiography": "xray",
}
WHY_ICON = ["badge", "smile", "grid", "lamp", "talk", "screen", "sterile"]
HOSPITAL_ICON = ["surgical", "pulse", "mask", "sterile"]
