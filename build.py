import os

SITE = os.path.dirname(os.path.abspath(__file__))

# Assets are self-hosted locally. Every raster image was downloaded from the
# live site and converted to .webp (see tools/fetch_and_optimize.py); videos
# were re-encoded for the web. asset() maps a live wp-content/uploads URL to
# its local .webp equivalent so the page markup stays readable.
UPLOADS = "https://amchealthcareinc.com/wp-content/uploads/"

def asset(url):
    """Live uploads URL -> local optimized webp path."""
    rel = url[len(UPLOADS):] if url.startswith(UPLOADS) else url
    base, _ext = os.path.splitext(rel)
    return "assets/img/" + base + ".webp"

LOGO = asset("https://amchealthcareinc.com/wp-content/uploads/2024/02/long-logo.png")
FOOTER_LOGO = asset("https://amchealthcareinc.com/wp-content/uploads/2024/09/AMC_Logo_Horizontal_Secondary_Dark-1024x91.png")
BANNER = asset("https://amchealthcareinc.com/wp-content/uploads/2024/09/AMC_Banner_3x6_page-0001-1024x512.jpg")

NAV_ITEMS = [
    ("About Us", "about-us.html", [("Leadership", "leadership.html"), ("Partners", "partners.html")]),
    ("Process", "process.html", []),
    ("Press", "press.html", []),
    ("Contact Us", "contact-us.html", []),
]

def render_nav(active):
    parts = []
    for label, href, children in NAV_ITEMS:
        cls = "has-children" if children else ""
        aria = ' aria-current="page"' if href == active else ""
        li = f'<li class="{cls}"><a href="{href}"{aria}>{label}</a>'
        if children:
            sub = "".join(f'<li><a href="{h}">{l}</a></li>' for l, h in children)
            li += f'<ul class="submenu">{sub}</ul>'
        li += "</li>"
        parts.append(li)
    return "\n        ".join(parts)

def header(active):
    return f"""  <header class="site-header">
    <div class="header-inner">
      <a class="logo" href="index.html"><img src="{LOGO}" alt="AMC Healthcare"></a>
      <button class="menu-toggle" aria-label="Toggle menu" onclick="document.querySelector('.main-nav').classList.toggle('open')">&#9776;</button>
      <nav class="main-nav" aria-label="Primary">
        <ul>
        {render_nav(active)}
        </ul>
      </nav>
    </div>
  </header>
"""

def footer():
    return f"""  <footer class="site-footer">
    <div class="container">
      <div class="footer-top">
        <div>
          <div class="footer-logo"><img src="{FOOTER_LOGO}" alt="AMC Healthcare"></div>
          <div class="footer-address">
            AMC Healthcare, Inc.<br>
            201 E. Kennedy Blvd., Suite 1611<br>
            Tampa, Florida 33602, US<br>
            <a href="tel:+18132481818">(813) 248-1818</a>
          </div>
        </div>
        <nav class="footer-nav" aria-label="Footer">
          <ul>
            <li><a href="about-us.html">About Us</a></li>
            <li><a href="leadership.html">Leadership</a></li>
            <li><a href="partners.html">Partners</a></li>
            <li><a href="process.html">Process</a></li>
            <li><a href="press.html">Press</a></li>
            <li><a href="contact-us.html">Contact Us</a></li>
            <li><a href="https://www.linkedin.com/in/brent-yessin-01a62230/" target="_blank" rel="noopener">LinkedIn</a></li>
          </ul>
        </nav>
      </div>
      <div class="footer-bottom">
        <span>&copy; 2026 AMC Healthcare &mdash; <a href="#">Privacy Policy</a></span>
        <span>Approximate clone for internal reference &mdash; original design by Onymous Media</span>
      </div>
    </div>
  </footer>
"""

def page(title, description, active, body, extra_head=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} - AMC Healthcare (clone)</title>
<meta name="description" content="{description}">
<link rel="stylesheet" href="css/style.css">
{extra_head}</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
{header(active)}
  <main id="main">
{body}
  </main>
{footer()}
</body>
</html>
"""

# ---------- ABOUT US ----------
# Title sits in its own plain white block above the banner (matches the live
# page's DOM order: H1, then image, then body copy) so the heading text never
# sits near/over the banner photo's own colors -- guarantees navy-on-white
# contrast regardless of what's in the image.
about_body = f"""    <div class="page-content" style="padding-bottom:0;">
      <div class="container">
        <div class="hero-title"><h1>About Us</h1></div>
      </div>
    </div>
    <section class="hero">
      <img src="{BANNER}" alt="AMC Healthcare modular hospital banner">
    </section>
    <div class="page-content">
      <div class="container">
        <p>AMC Healthcare was founded by industry veterans and innovators to make the seemingly impossible immediately achievable: improve quality, enhance access and reduce the costs of providing healthcare.</p>
        <p>We challenge conventional construction and design concepts that add cost and time to the provision of vital health services. It takes too long to build hospitals, it costs too much to design them and open them, and it makes financing needed additions or replacements cost prohibitive.</p>
        <p>Health systems around the world struggle to increase access and quality while containing costs. Those challenges are worse when natural disasters and regional conflict intervene to destroy facilities, disrupt building projects and obstruct supply chains.</p>
        <p>People have been building airplanes inside since the Wright Brothers built the first &ldquo;flying machine&rdquo; in a bicycle shop in North Carolina&hellip; yet we have persisted in building hospitals in open fields, slowed by weather and unavailability of labor or supplies. AMC veterans changed all that, building the first inpatient, acute care hospital in a factory, and opening it in record time.</p>
        <p>Now, the race is on to standardize that process, to continuously improve it, and to provide US quality healthcare facilities around the globe &ndash; and throughout underserved areas of the United States. AMC is leading that race.</p>
        <p class="contact-note">For inquiries regarding AMC Healthcare, please contact: Brent Yessin, General Counsel</p>
      </div>
    </div>
"""

# ---------- PROCESS ----------
process_images = [
    "https://amchealthcareinc.com/wp-content/uploads/2024/12/IMG_3339-rotated.jpg",
    "https://amchealthcareinc.com/wp-content/uploads/2024/12/IMG_3352-rotated.jpg",
    "https://amchealthcareinc.com/wp-content/uploads/2024/09/TFMCviewfromMainStreet-copy_3-1.jpg",
    "https://amchealthcareinc.com/wp-content/uploads/2024/12/AMC-Hospital-Shot-Outter-V1.png",
    "https://amchealthcareinc.com/wp-content/uploads/2024/12/AMC-Hospital-Shot-Inner-V2.png",
    "https://amchealthcareinc.com/wp-content/uploads/2024/09/unit-being-set-on-pier-and-beam.png",
]
process_gallery = "\n          ".join(f'<img src="{asset(u)}" alt="AMC Healthcare construction process" loading="lazy">' for u in process_images)

process_body = f"""    <div class="page-content">
      <div class="container">
        <div class="hero-title"><h1>Process</h1></div>
        <p>Every project begins with planning &ndash; functional planning and logistics. Listening to your needs. Designing to your needs with best practices in mind. Site work begins even before the final plan is complete.</p>
        <p>Building in the plant begins while foundations are being poured. Delivery and assembly takes days and weeks not months or years, and commissioning happens within a month of modules being set.</p>
        <div class="gallery-grid">
          {process_gallery}
        </div>
      </div>
    </div>
"""

# ---------- PRESS ----------
press_items = [
    ("September 18, 2024", "George Pataki and Partners Launch Multi-Million Dollar Effort to Build Hospitals in War-Torn Ukraine",
     "Former New York Governor George Pataki has announced a multi-million dollar fundraising campaign to support the construction of modular hospitals…",
     "https://amchealthcareinc.com/george-pataki-and-partners-launch-multi-million-dollar-effort-to-build-hospitals-in-war-torn-ukraine/"),
    ("June 15, 2024", "Albany Mayor Kathy Sheehan Joins Bucha Mayor Anatolii Fedoruk and Scores of Volunteers",
     "“BUCHA, UKRAINE – Albany Mayor Kathy Sheehan joined Bucha Mayor Anatolii Fedoruk on Friday, June 14 to help deliver 40+ ambulances…",
     "https://amchealthcareinc.com/albany-mayor-kathy-sheehan-joins-bucha-mayor-anatolii-fedoruk-and-scores-of-volunteers/"),
    ("May 3, 2024", "House Foreign Affairs Chairman Urges USAID to Fund Hospital Reconstruction in War-Torn Ukraine",
     "House Foreign Affairs Committee Chairman Michael T. McCaul has urged USAID Administrator Samantha Power to allocate funds from the recently…",
     "https://amchealthcareinc.com/house-foreign-affairs-chairman-urges-usaid-to-fund-hospital-reconstruction-in-war-torn-ukraine/"),
    ("January 13, 2024", "Oleksiy Kuleba, Viktor Liashko met with representatives of American medical, charitable organizations",
     "“Deputy Head of the Office of the President of Ukraine Oleksiy Kuleba and Minister of Health of Ukraine Viktor Liashko…",
     "https://amchealthcareinc.com/oleksiy-kuleba-viktor-liashko-met-with-representatives-of-american-medical-charitable-organizations-who-presented-the-concept-of-building-several-healthcare-facilities/"),
]

press_html = "\n".join(f"""        <article class="press-item">
          <span class="date">{d}</span>
          <h2><a href="{u}" target="_blank" rel="noopener">{t}</a></h2>
          <p>{s}</p>
          <a class="read-more" href="{u}" target="_blank" rel="noopener">Read More &rarr;</a>
        </article>""" for d, t, s, u in press_items)

press_body = f"""    <div class="page-content">
      <div class="container">
        <div class="hero-title"><h1>Press</h1></div>
{press_html}
      </div>
    </div>
"""

# ---------- CONTACT US ----------
contact_body = """    <div class="page-content">
      <div class="container">
        <span class="eyebrow">We&rsquo;re Here To Help</span>
        <h1>Have Questions? Reach Out</h1>
        <p>For inquiries regarding AMC Healthcare or AMC Pharma-USA, please contact: Brent Yessin, General Counsel. Or fill out the form below.</p>
        <div class="contact-details">
          <div>
            <h5>Email</h5>
            <a href="mailto:byessin@amcpharma-usa.com">byessin@amcpharma-usa.com</a>
          </div>
          <div>
            <h5>Phone</h5>
            <a href="tel:+18132481818">(813) 248-1818</a>
          </div>
          <div>
            <h5>Address</h5>
            201 E. Kennedy Blvd., Suite 1611<br>Tampa, Florida 33602, US
          </div>
        </div>
        <form class="contact-form" onsubmit="alert('This is a static clone \\u2014 form submission is not wired up.'); return false;">
          <div class="field-row">
            <div><label for="fname">First Name</label><input id="fname" type="text" required></div>
            <div><label for="lname">Last Name</label><input id="lname" type="text" required></div>
          </div>
          <label for="email">Email</label>
          <input id="email" type="email" required style="margin-bottom:16px;">
          <label for="phone">Phone</label>
          <input id="phone" type="tel" required style="margin-bottom:16px;">
          <label for="message">Message</label>
          <textarea id="message" required></textarea>
          <div style="margin-top:16px;"><button type="submit">Submit</button></div>
          <p class="form-note">Static demo form &mdash; wire up to Netlify Forms or a form service before going live.</p>
        </form>
      </div>
    </div>
"""

# ---------- LEADERSHIP ----------
leaders = [
    ("Brent W. Yessin, Esq.", "https://amchealthcareinc.com/wp-content/uploads/2024/09/Brent_Yessin_Edit-square.jpg"),
    ("Graham Russell, RN", "https://amchealthcareinc.com/wp-content/uploads/2024/09/Graham_Russell-square.jpeg"),
    ("Joe Edwards", "https://amchealthcareinc.com/wp-content/uploads/2026/01/1758167803794.jpg"),
    ("Brett Scott, Esq.", "https://amchealthcareinc.com/wp-content/uploads/2024/09/Brett_Scott-Modified-square.jpeg"),
    ("Jim Cusack, Esq.", "https://amchealthcareinc.com/wp-content/uploads/2024/09/Jim_Cusack-Modified-square-scaled.jpeg"),
    ("Robin Austin, IIDA", "https://amchealthcareinc.com/wp-content/uploads/2025/02/IMG_2606.jpg"),
    ("Sylwia Fitch, Country Manager – Europe", "https://amchealthcareinc.com/wp-content/uploads/2025/07/IMG_4628.jpg"),
    ("Robert D. Swain", "https://amchealthcareinc.com/wp-content/uploads/2026/05/Essex-Capital-Group-Rob-Swain-1-600x600-1.jpg"),
]

leaders_html = "\n          ".join(f"""<div class="person-card">
            <img src="{asset(img)}" alt="{name}" loading="lazy">
            <h3>{name}</h3>
          </div>""" for name, img in leaders)

leadership_body = f"""    <div class="page-content">
      <div class="container">
        <div class="hero-title"><h1>AMC Leadership</h1></div>
        <div class="people-grid">
          {leaders_html}
        </div>
      </div>
    </div>
"""

# ---------- PARTNERS ----------
partners = [
    ("Madison Industries", "https://www.madisonind.com/"),
    ("Modular Services Company", "https://modularservices.com/"),
    ("B. Frank Studio", "https://bfrankstudio.com/"),
    ("Northwell Health", "https://www.northwell.edu/"),
    ("The George Pataki Center", "https://www.georgepatakicenter.com/"),
    ("Globalux", "https://golbalux.pl/pl"),
    ("Promostal", "https://promostal.pl/en/"),
    ("Ukraine Focus – Volunteer Ambulance Corps", "https://ukrainefocus.org/volunteer-ambulance-corps/"),
]

partners_html = "\n          ".join(f'<a href="{u}" target="_blank" rel="noopener">{n}</a>' for n, u in partners)

partners_body = f"""    <div class="page-content">
      <div class="container">
        <div class="hero-title"><h1>Partners</h1></div>
        <p>Click a partner to learn more.</p>
        <div class="partner-logos">
          {partners_html}
        </div>
      </div>
    </div>
"""

# ---------- HOME ----------
# Video hero uses the self-hosted, re-encoded logo-animation loop (autoplay,
# muted, playsinline so it loops silently as a background) with a poster frame
# for the pre-load paint. The larger promo films are click-to-play with posters
# and preload="none" so they never touch the initial page load.
home_body = f"""    <section class="video-hero">
      <video class="video-hero-bg" autoplay muted loop playsinline
             poster="assets/video/logo-animation-poster.webp">
        <source src="assets/video/logo-animation.webm" type="video/webm">
        <source src="assets/video/logo-animation.mp4" type="video/mp4">
      </video>
      <div class="video-hero-overlay"></div>
      <div class="container video-hero-content">
        <h1>Modular Healthcare Solutions</h1>
        <p>Controlled Environment Construction cuts delivery time by 50&ndash;75% and costs by up to 50%, bringing US-quality healthcare facilities online faster &ndash; in underserved regions of the US and around the globe.</p>
        <a class="btn" href="contact-us.html">Contact Us</a>
      </div>
    </section>
    <section class="stat-strip">
      <div class="stat"><h3>Rapid Deployment &amp; Scalability</h3><p>Controlled Environment Construction cuts delivery time by 50% to 75%</p></div>
      <div class="stat"><h3>Cost Effectiveness</h3><p>Controlled Environment Construction cuts costs up to 50%</p></div>
      <div class="stat"><h3>Flexibility and Customization</h3><p>Customized facilities according to the specific needs of the community</p></div>
      <div class="stat"><h3>Quality and Compliance</h3><p>Built to US and Joint Commission International Standards</p></div>
    </section>
    <div class="page-content">
      <div class="container">
        <h2>Healthcare Can&rsquo;t Wait</h2>
        <p>AMC Healthcare is restoring access to care with permanent modular hospitals built faster and smarter. The first modular inpatient units in the USA were built by AMC executives, transported 1,000 miles and reassembled &ndash; the first surgery took place 28 days after the modules were set.</p>
        <div class="feature-video">
          <video controls preload="none" poster="assets/video/hospital-film-poster.webp">
            <source src="assets/video/hospital-film.mp4" type="video/mp4">
          </video>
        </div>
      </div>
    </div>
    <section class="film-strip">
      <div class="container">
        <h2>Our Story</h2>
        <div class="film-grid">
          <figure class="film">
            <video controls preload="none" poster="assets/video/amc-60-poster.webp">
              <source src="assets/video/amc-60.mp4" type="video/mp4">
            </video>
            <figcaption>AMC in 60 Seconds</figcaption>
          </figure>
          <figure class="film">
            <video controls preload="none" poster="assets/video/america-first-poster.webp">
              <source src="assets/video/america-first.mp4" type="video/mp4">
            </video>
            <figcaption>America First</figcaption>
          </figure>
        </div>
      </div>
    </section>
"""

pages = [
    ("index.html", "Home", "AMC Healthcare — modular healthcare construction delivered faster and at lower cost through Controlled Environment Construction.", None, home_body),
    ("about-us.html", "About Us", "About AMC Healthcare — approximate clone of the live About Us page.", "about-us.html", about_body),
    ("process.html", "Process", "AMC Healthcare's modular construction process — approximate clone.", "process.html", process_body),
    ("press.html", "Press", "AMC Healthcare press coverage — approximate clone.", "press.html", press_body),
    ("contact-us.html", "Contact Us", "Contact AMC Healthcare — approximate clone.", "contact-us.html", contact_body),
    ("leadership.html", "Leadership", "AMC Healthcare leadership team — approximate clone.", "about-us.html", leadership_body),
    ("partners.html", "Partners", "AMC Healthcare partners — approximate clone.", "about-us.html", partners_body),
]

os.makedirs(SITE, exist_ok=True)
for fname, title, desc, active, body in pages:
    html = page(title, desc, active, body)
    with open(os.path.join(SITE, fname), "w", encoding="utf-8") as f:
        f.write(html)

print("Built", len(pages), "pages into", SITE)
