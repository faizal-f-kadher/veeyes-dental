# Structured, cleaned copy for the Veeyes Dental redesign.
# Source: the clinic's own site (scraped into veeyes_site/). Copy has been lightly
# edited for grammar, repetition and stray SEO text; facts are unchanged.

W = "https://static.wixstatic.com/media/"

def wix(path, w=900):
    """Rebuild a Wix CDN URL at a larger size. path = '<id>~mv2.jpg' or with '/v1/crop/...'."""
    if "/v1/" in path:
        base, rest = path.split("/v1/", 1)
        crop = ""
        if rest.startswith("crop/"):
            crop = rest.split("/fill")[0] + "/"
        return f"{W}{base}/v1/{crop}fit/w_{w},h_{w},q_90/img.jpg"
    return f"{W}{path}/v1/fit/w_{w},h_{w},q_90/img.jpg"

LOGO = W + "1eb75c_cd55877863ff44ac9041dbded5f86359~mv2.png/v1/fit/w_640,h_260,q_95/veeyes-logo.png"
LOGO_FAVICON = W + "1eb75c_cd55877863ff44ac9041dbded5f86359~mv2.png/v1/crop/x_0,y_0,w_3190,h_3190/fit/w_128,h_128/veeyes-mark.png"

# Free stock video. Pexels License and Mixkit Free License: free for commercial use, no attribution required.
PX = "https://videos.pexels.com/video-files/"
VIDEO = {
    "hero":    {"src": PX + "7803018/7803018-hd_1920_1078_30fps.mp4", "small": PX + "7803018/7803018-sd_960_540_30fps.mp4",
                "poster": "https://images.pexels.com/videos/7803018/dental-clinic-dentistry-7803018.jpeg", "page": "https://www.pexels.com/video/a-dnttist-relaxing-her-young-patient-7803018/"},
    "clinic":  {"src": PX + "6763242/6763242-hd_1920_1080_25fps.mp4", "small": PX + "6763242/6763242-sd_960_540_25fps.mp4",
                "poster": "https://images.pexels.com/videos/6763242/aching-tooth-clinic-computer-dentist-6763242.jpeg", "page": "https://www.pexels.com/video/video-of-a-dental-clinic-6763242/"},
    "consult": {"src": PX + "4490544/4490544-hd_1280_720_50fps.mp4", "small": PX + "4490544/4490544-sd_960_540_25fps.mp4",
                "poster": "https://images.pexels.com/videos/4490544/pexels-photo-4490544.jpeg", "page": "https://www.pexels.com/video/woman-getting-dental-cleaning-4490544/"},
    "xray":    {"src": PX + "5356055/5356055-hd_720_1280_25fps.mp4", "small": PX + "5356055/5356055-sd_540_960_25fps.mp4",
                "poster": "https://images.pexels.com/videos/5356055/pexels-photo-5356055.jpeg", "page": "https://www.pexels.com/video/a-dentist-explaining-a-dental-x-ray-5356055/"},
    "treat":   {"src": PX + "5356196/5356196-hd_1280_720_25fps.mp4", "small": PX + "5356196/5356196-sd_960_540_25fps.mp4",
                "poster": "https://images.pexels.com/videos/5356196/pexels-photo-5356196.jpeg", "page": "https://www.pexels.com/video/female-dentist-working-with-patient-5356196/"},
    "kids":    {"src": PX + "7803498/7803498-hd_720_1280_60fps.mp4", "small": PX + "7803498/7803498-sd_540_960_30fps.mp4",
                "poster": "https://images.pexels.com/videos/7803498/adult-affection-baby-beautiful-7803498.jpeg", "page": "https://www.pexels.com/video/a-girl-at-a-dental-clinic-7803498/"},
    "braces":  {"src": "https://assets.mixkit.co/videos/24630/24630-720.mp4", "small": "https://assets.mixkit.co/videos/24630/24630-360.mp4",
                "poster": "https://assets.mixkit.co/videos/24630/24630-thumb-720-0.jpg", "page": "https://mixkit.co/free-stock-video/woman-with-braces-smiling-24630/"},
    "whitening": {"src": "https://assets.mixkit.co/videos/39580/39580-720.mp4", "small": "https://assets.mixkit.co/videos/39580/39580-360.mp4",
                "poster": "https://assets.mixkit.co/videos/39580/39580-thumb-720-0.jpg", "page": "https://mixkit.co/free-stock-video/man-on-a-teeth-whitening-procedure-with-the-dentist-39580/"},
}

CLINICS = [
    {
        "city": "Coimbatore",
        "tag": "Head office",
        "address": ["Sathy Main Road, Ramakrishna Mill Bus Stop", "Ramakrishnapuram, Ganapathy", "Coimbatore, Tamil Nadu 641006"],
        "phones": [("0422 253 3333", "+914222533333"), ("+91 88256 18228", "+918825618228")],
        "whatsapp": "918825618228",
        "email": "veeyesdentalhospital@gmail.com",
        "map": "https://www.google.com/maps/search/?api=1&query=Veeyes+Dental+Hospital+Ganapathy+Coimbatore",
    },
    {
        "city": "Tiruppur",
        "tag": "Where we started, 2004",
        "address": ["Avinashi – Tiruppur Main Road, Bunglow Bus Stop", "Indira Nagar, near CSI Church", "Tiruppur, Tamil Nadu 641603"],
        "phones": [("0421 433 3366", "+914214333366"), ("+91 93447 28252", "+919344728252")],
        "whatsapp": "919344728252",
        "email": "info@veeyesdental.com",
        "map": "https://www.google.com/maps/search/?api=1&query=Veeyes+Dental+Hospital+Tiruppur",
    },
]

SOCIAL = [
    ("Instagram", "https://www.instagram.com/veeyes_dental_hospital/"),
    ("Facebook", "https://facebook.com/veeyesdentalhospital"),
    ("LinkedIn", "https://www.linkedin.com/in/veeyes-dental-hospital-51946626b"),
]

FACTS = [
    ("2004", "First practice opens in Tiruppur"),
    ("2", "Hospitals, Coimbatore and Tiruppur"),
    ("14", "Operatory dental chairs"),
    ("6,500", "Sq. ft of clinical space"),
    ("22", "Dental specialists on the team"),
]

# ---------------------------------------------------------------- before / after
# Pairs from the Smile Gallery, in the order the old site showed them.
_G = [
 ("Teeth alignment", [("d6c03a_d8dfb263ea85468686419aab180c7e2a~mv2.jpeg", "d6c03a_d72bba5ff1cf4a6aad0d4af1256acd32~mv2.jpeg"),
                      ("d6c03a_a884f6a8dd924dedba999c8574d8670a~mv2.jpeg", "d6c03a_c496b4f8696e45faa1eb2478c6173601~mv2.jpeg"),
                      ("d6c03a_ddc773259cc14022b1875c06d310603d~mv2.jpeg", "d6c03a_d6194f9b013049ceb1e277957d83578b~mv2.jpeg")]),
 ("Crowns", [("d6c03a_e3ad86a6f0f74ac881677b8ef55fe448~mv2.jpg", "d6c03a_adcd2e5e85f04e76976dd8d89d4eca17~mv2.jpg"),
             ("d6c03a_640079fd2f194dc78baffe3d3d80ff2e~mv2.jpg/v1/crop/x_51,y_35,w_655,h_329/fill", "d6c03a_640079fd2f194dc78baffe3d3d80ff2e~mv2.jpg/v1/crop/x_48,y_385,w_657,h_363/fill"),
             ("d6c03a_cfb1f5c1439d48b09f90e6b0b53c21b2~mv2.jpeg/v1/crop/x_0,y_6,w_444,h_223/fill", "d6c03a_cfb1f5c1439d48b09f90e6b0b53c21b2~mv2.jpeg/v1/crop/x_0,y_264,w_444,h_245/fill")]),
 ("Veneers", [("d6c03a_7530a7882e9d468193d8e3d8a225b170~mv2.jpeg/v1/crop/x_0,y_15,w_407,h_213/fill", "d6c03a_4ec7c4452a3442a291c873535e1bfe7e~mv2.jpg/v1/crop/x_0,y_15,w_407,h_213/fill")]),
 ("Inlay", [("d6c03a_32824f3023b94b74b668a2cbdfeb7705~mv2.jpeg/v1/crop/x_0,y_29,w_1280,h_642/fill", "d6c03a_e3dfe915e4b74499abd85e58814fdadb~mv2.jpeg/v1/crop/x_0,y_145,w_1280,h_708/fill")]),
 ("Overlay", [("d6c03a_eb51eb6a26994387b7ef0744a02b093b~mv2.jpeg/v1/crop/x_0,y_0,w_1089,h_630/fill", "d6c03a_eb51eb6a26994387b7ef0744a02b093b~mv2.jpeg/v1/crop/x_0,y_650,w_1089,h_630/fill"),
              ("d6c03a_67f32619100747bc940659b69f0e827b~mv2.jpg/v1/crop/x_0,y_303,w_1080,h_555/fill", "d6c03a_566052f6af40460faa6939b741c79ce9~mv2.jpg/v1/crop/x_18,y_302,w_1044,h_600/fill")]),
 ("Teeth in an hour", [("d6c03a_9fac9c5a57894661bd58216fe00a1b68~mv2.jpg", "d6c03a_e396180a1ba94158baf19818343aa43e~mv2.jpg")]),
 ("Cosmetic dentistry", [("d6c03a_902cc52074164feb9a5b43d6e466f4db~mv2.jpg", "d6c03a_1446c091d77442cfbc3abe874d3e8fc7~mv2.jpeg")]),
 ("Laser gum treatment", [("d6c03a_08b78f3deab44d9a86dd389244ce7e77~mv2.jpg", "d6c03a_d9899e0126104dfe9fa95987209bb264~mv2.jpg")]),
 ("Smile designing", [("d6c03a_4937ab0685a144c495756846d2bdfbc4~mv2.jpg", "d6c03a_e031bc1c756e4c98b377a40ec61ff3fc~mv2.jpg")]),
 ("Tooth fracture", [("d6c03a_93d99f9384a84ca1b69e397d8265040f~mv2.jpeg/v1/crop/x_0,y_0,w_1080,h_543/fill", "d6c03a_93d99f9384a84ca1b69e397d8265040f~mv2.jpeg/v1/crop/x_80,y_568,w_927,h_512/fill")]),
 ("Front tooth filling", [("d6c03a_8e0493178e384ac298828b6463967e63~mv2.jpeg/v1/crop/x_59,y_0,w_1148,h_577/fill", "d6c03a_8e0493178e384ac298828b6463967e63~mv2.jpeg/v1/crop/x_68,y_590,w_1081,h_597/fill")]),
 ("Back tooth filling", [("d6c03a_20b6e46cd482490c978026f002e445e1~mv2.jpeg", "d6c03a_42acf3b227554b59bf7ce744817ef9db~mv2.jpeg")]),
 ("Gum treatment", [("d6c03a_2b11dd4d70b348148c1d070f14661d9e~mv2.jpeg/v1/crop/x_0,y_0,w_1080,h_543/fill", "d6c03a_2b11dd4d70b348148c1d070f14661d9e~mv2.jpeg/v1/crop/x_58,y_557,w_946,h_523/fill"),
                    ("d6c03a_2c775193dcfe41788cd0e88a713e1c30~mv2.jpeg/v1/crop/x_35,y_0,w_1196,h_601/fill", "d6c03a_2c775193dcfe41788cd0e88a713e1c30~mv2.jpeg/v1/crop/x_115,y_596,w_1056,h_583/fill")]),
 ("Full mouth rehabilitation", [("d6c03a_84cff63f059640d683aa358616019195~mv2.jpeg/v1/crop/x_0,y_0,w_1280,h_644/fill", "d6c03a_84cff63f059640d683aa358616019195~mv2.jpeg/v1/crop/x_30,y_546,w_1220,h_674/fill"),
                                ("d6c03a_f69bd5d84b5a40759cc6ca4072050e12~mv2.jpeg", "d6c03a_c1017f5abded485393648fdb000021eb~mv2.jpeg")]),
]
# Single combined before/after photos (no separate pair)
SINGLES = [
 ("Wisdom tooth removal", "d6c03a_f4a6a3e88e2642faa0784fea6127e33a~mv2.jpg"),
 ("Preventive dentistry", "d6c03a_9b414e49b4314152896bc25d3678d4ce~mv2.jpg/v1/crop/x_20,y_20,w_360,h_193/fill"),
]
GALLERY = [(name, [(wix(b, 1000), wix(a, 1000)) for b, a in pairs]) for name, pairs in _G]
GALLERY_BY = dict(GALLERY)

CLINIC_PHOTOS = [wix(p, 1200) for p in [
 "58e191_55d1e35ccc0a4360baf5f69bc4af27c7~mv2.jpg", "1eb75c_6bcedfbc5cbd42519d8a09309264ac73~mv2.jpeg",
 "58e191_bb608a5e4d8243bc9a9eb5c91f4eaaeb~mv2.jpg", "1eb75c_7a08284e4c37471eac6b4d62af31c29f~mv2.jpeg",
 "58e191_dab4f3738d2e4091861b3396d9a2117e~mv2.png", "58e191_3044dffaa0884919bd0d321aec0292ed~mv2.jpg",
 "58e191_734c09a2a4d7461b96e45771806b8c93~mv2.jpg", "58e191_646a896b8c4747aea2b312f99133c4c6~mv2.jpg",
 "58e191_12034b5b54a94a5b8443d31ca0c0c44a~mv2.jpeg", "d6c03a_a1381d8a3fb64924b0041dc35f6e8fd5~mv2.jpg",
 "d6c03a_37b6db1cad0246a3b39cd7a0726ae23d~mv2.jpg", "d6c03a_89a668196fca4fdcaf60c46b482e5422~mv2.jpg",
 "d6c03a_10c3bfac3030459490fef81ceb755932~mv2.jpg", "d6c03a_53735f47fbac4bd7845dad94a67e0f45~mv2.jpg",
 "d6c03a_d89f7de060a3459183364d855a9c02cc~mv2.jpg", "d6c03a_6a7a105cbe684092bafa99ba3eafdac6~mv2.jpg",
 "d6c03a_0110413ed08c40b5a69b6276c3f13415~mv2.jpg",
]]

PH = dict(zip(["building","corridor","waiting_invisalign","reception","kids_tree","waiting","kids_stars","operatory_wood","ot",
                "signage_night","waiting_room","operatory_1","operatory_2","operatory_3","front_desk","operatory_4","cbct"], CLINIC_PHOTOS))
PH_ALT = {"building": "Veeyes Dental Hospital building", "corridor": "Hospital corridor at Veeyes", "waiting_invisalign": "Patients in the Veeyes waiting area, Invisalign provider sign",
  "reception": "Reception and waiting area at Veeyes", "kids_tree": "Children's treatment room with tree mural", "waiting": "Patients in the waiting hall",
  "kids_stars": "Children's treatment room with star mural", "operatory_wood": "Treatment room with dental chair", "ot": "Dental surgery in the Veeyes operation theatre",
  "signage_night": "Veeyes Dental Care Advanced Implant Center signage", "waiting_room": "Waiting lounge", "operatory_1": "Dental chair in a treatment room",
  "operatory_2": "Treatment room with two dental chairs", "operatory_3": "Treatment room", "front_desk": "Front desk", "operatory_4": "Treatment room with dental chair and monitor",
  "cbct": "CBCT and OPG imaging machine"}

# ---------------------------------------------------------------- people
LEADS = [
 {"name": "Dr. Ramesh Shanmugam", "role": "M.D.S · Clinical Director, Orthodontist", "img": wix("58e191_9ed8f759609c464ba9260b5dd28600f6~mv2.jpeg", 700),
  "short": "Over 24 years as a clinician, academician and researcher, with a focus on orthodontics and oral implantology.",
  "bio": [
   "Dr. Ramesh is a seasoned dental surgeon with over twenty-four years of experience as a clinician, academician, researcher and administrator, with significant work in orthodontics and oral implantology. He runs the two Veeyes multi-speciality centres in Coimbatore and Tiruppur.",
   "He holds a master's in dental surgery in Orthodontics and Dentofacial Orthopaedics, is an Honorary Diplomate of the Indian Board of Orthodontics, and is a certified Oral Implantologist from Manipal. He specialises in periodontal surgery and lingual and contemporary orthodontics, and is skilled in root canals, cosmetic dentistry and implants.",
   "He has taught as a professor at Sri Ramakrishna Dental College & Hospital and RVS Dental College & Hospital, consults with KG Hospital in Coimbatore, and has contributed to work on dental ethics, jurisprudence and interdisciplinary dentistry.",
  ]},
 {"name": "Dr. Ranjana Ramesh", "role": "M.D.S · Cosmetic Dentist, BPS Specialist", "img": wix("d6c03a_05b0a4416adc4071a1b2605381a3cf62~mv2.jpg", 700),
  "short": "Cosmetic dentist and Biofunctional Prosthetic System specialist with over 16 years of practice.",
  "bio": [
   "Dr. Ranjana is a cosmetic dentist, surgeon and BPS (Biofunctional Prosthetic System) specialist with over 16 years of experience in Chennai, Coimbatore and Tiruppur. Patients consult her from across the country and abroad.",
   "Alongside cosmetic dentistry and BPS dentures she specialises in full mouth rehabilitation, laser and implant dentistry, and has presented award-winning papers at national and international conferences.",
   "She completed her Bachelor's and Master's in Dental Surgery at Dr. MGR Medical University, was a Gold Medallist in Oral Anatomy and Histology, and received the International PFA Senior Student Award from the Pierre Fauchard Academy. She is known for her patience with children and elderly patients.",
  ]},
]
_team_imgs = ["58e191_4504e2d99ae949ef87d1cee712bfa371~mv2.png","58e191_ed8d07f0fade4c75848acc8653ca92b1~mv2.png","58e191_f0e7e09f205746b690a7276068be4b83~mv2.png",
 "58e191_9549b29ea4d84a509148fc084efd5c77~mv2.png","58e191_d37bd1766954413e84a50b653817b96b~mv2.png","58e191_71c9d5dbafeb4a1ca7322d8d686608f0~mv2.png",
 "58e191_258e4824f34a4b92ade1cd9dc55d701a~mv2.png","58e191_69469e194bc34bfeb3755fdc1d599df6~mv2.png/v1/crop/x_0,y_282,w_1845,h_1845/fill","58e191_60e8bc897afa46d78365a085682e95c3~mv2.png",
 "58e191_c14de55571154a539ee5fa9ff96762e1~mv2.png","58e191_607e34352c9741c7aad4e50775cc539a~mv2.png","58e191_27514455842449119f032c30915bfedf~mv2.png",
 "58e191_8001b004a7844e2db1d2cc1c5e074c5a~mv2.png","58e191_31eff23d06c443708886f7de91a9840f~mv2.png"]
_team = [("Dr. Shalini","Endodontist"),("Dr. Sabitha","General Dentist"),("Dr. Thivya Shankari","Endodontist"),("Dr. Shwetha","General Dentist"),
 ("Dr. Ashwini","Pedodontist"),("Dr. Angelin","Periodontist"),("Dr. Geetha","General Dentist"),("Dr. Glory","General Dentist"),
 ("Dr. Sharath","Oral Medicine & Radiology"),("Dr. Sathya","General Dentist"),("Dr. Nakshatra","General Dentist"),("Dr. Gayathri","Pedodontist"),
 ("Dr. Vishnu Priya","General Dentist"),("Dr. Asha V Shet","Oral & Maxillofacial Surgeon")]
_team_files = ["shalini","sabitha","thivya","shwetha","ashwini","angelin","geetha","glory","sharath","sathya","nakshatra","gayathri","vishnu-priya","asha"]
TEAM = [{"name": n, "role": r, "img": wix(i, 400)} for (n, r), i in zip(_team, _team_imgs)]

# (quote, name, place, tags) - tags are (label, link) taken from what the patient mentions
REVIEWS = [
 ("Excellent services and friendly staff. I went for braces treatment for my daughter. Dr. Ramesh is very professional and I would recommend him.", "Kowsalya J", "Coimbatore",
  [("Braces for her daughter", "teeth-alignment.html"), ("Dr. Ramesh", "about.html#ramesh")]),
 ("Doctor Ranjana is very polite and kind enough to answer your queries. She knows what she is doing and won't ask you to take up procedures you don't need. I would recommend her and Dr. Ramesh.", "Raja", "Coimbatore",
  [("Dr. Ranjana", "about.html#ranjana"), ("Dr. Ramesh", "about.html#ramesh")]),
 ("The entire consultation was very professional and pleasant. They have their expert touch in every step of treatment. Highly recommended.", "Pradeepan", "Coimbatore",
  [("Consultation", "appointment.html")]),
]
GOOGLE_REVIEWS = "https://www.google.com/maps/search/?api=1&query=Veeyes+Dental+Hospital+Coimbatore"

WHY = [
 ("Quality treatment", "A professional, friendly environment is one of the main reasons our patients keep coming back."),
 ("Aesthetics and function", "Eating, speaking, laughing: it all happens in your mouth, and your smile is where first impressions are made. We plan for both looks and function."),
 ("Multi-speciality under one roof", "Implants, dentures, veneers, simple and complex extractions, Invisalign and cosmetic work, handled by specialists in a single facility."),
 ("State-of-the-art equipment", "3D CBCT imaging, a Trios 3D intra-oral scanner, dental lasers, microscopic endodontics and a piezo bone-surgery unit."),
 ("Patient management", "Civility, respect, patience and kindness. Our dentists answer every question, however simple, and explain each plan until you fully understand it."),
 ("Digital dentistry", "Digital records, RVG, OPG, lateral cephalograms and CBCT for diagnosis, plus digital smile design, digital impressions and CAD/CAM crowns."),
 ("Five-step sterilisation", "Trained dental assistants follow a five-step sterilisation protocol for every instrument, chair and operatory, in line with international standards."),
]

AREAS = ["Sathyamangalam", "Annur", "Karamadai", "Mettupalayam", "Erode", "Ooty", "Salem"]

# ---------------------------------------------------------------- treatments
# Each: slug (matches the old URL), name, group, summary (card line), lead, sections, ba (gallery keys), video
GROUPS = [
 ("straighten", "Straighten"),
 ("replace", "Replace & rebuild"),
 ("cosmetic", "Cosmetic"),
 ("everyday", "Everyday & family care"),
 ("digital", "Diagnostics & technology"),
]

T = []
def t(**k): T.append(k)

t(slug="teeth-alignment", name="Teeth Alignment", group="straighten", video="braces", ba=["Teeth alignment"],
  summary="Metal, ceramic and lingual braces, aligners and early orthodontics.",
  lead="Crooked teeth and gaps are common in children and adults alike. Thumb sucking, tongue thrusting, jaw position, genetics or an old injury can all play a part, and it is never too late to straighten a smile. Our orthodontists offer braces, growth-guiding appliances and, where needed, surgical jaw correction.",
  sections=[
   ("Regular metal braces", ["The most widely used braces for children and young adults. Small pre-programmed metal brackets are bonded to the teeth and joined by a thin wire that moves them into place. Elastic bands hold the wire and are adjusted monthly. Cost-effective and reliable."], []),
   ("Self-ligating metal braces", ["These look like regular metal braces, but special clips hold the wire instead of elastic bands. The force is low and continuous, so they work efficiently, need fewer visits and less chair time, and are easier to clean. We use systems such as Damon (Ormco) and Empower (American Orthodontics)."], []),
   ("Ceramic self-ligating braces", ["Clear or tooth-coloured brackets that are far less noticeable than metal, popular with teenagers and adults. Results are the same as self-ligating metal braces. We use Clarity SL."], []),
   ("Lingual braces", ["Bonded to the inside surfaces of your teeth and custom made with CAD/CAM to fit their contours. They take a little getting used to but are as effective as regular braces, and are truly invisible to anyone but you and your orthodontist. Often chosen by adults over 30."], []),
   ("Invisalign and clear aligners", ["A no-braces option: a series of custom-made, near-invisible aligners that move your teeth gradually. Suitable for teens and adults with less severe problems, as long as the aligners are worn consistently. Similar systems include ClearPath, K-Line, ClearCorrect and Flex-Align."], []),
   ("Interceptive orthodontics", ["Diagnosing and treating misplaced teeth and uneven jaw growth early, while permanent teeth are still coming in. Dentofacial orthopaedics, often called Myobraces, uses appliances such as the Activator, Frankel, Bionator and Twin Block to improve oral muscle function, harmonise jaw growth and guide eruption.", "Once jaw growth is complete, skeletal bite problems can be corrected surgically through orthognathic surgery."], []),
  ])

t(slug="invisalign", name="Invisalign", group="straighten", video="braces", ba=[], old="copy-of-inflation-facility-1",
  summary="Clear, removable aligners planned around your teeth.",
  lead="Invisalign straightens teeth without traditional braces. A series of virtually invisible, custom-made aligners gently shifts your teeth into place with very little disruption to daily life.",
  sections=[
   ("Why patients choose Invisalign", [], [("Clear and comfortable", "The aligners are virtually invisible and discreet."), ("Removable", "Take them out to eat, brush, or for special occasions."), ("Made for your teeth", "Each set is custom made to fit comfortably and move your teeth in planned steps.")]),
   ("Our approach", ["Your Invisalign journey starts with a full consultation with our orthodontists, who build a personalised treatment plan around the smile you want. Regular check-ups keep progress on track, with adjustments made as needed."], []),
  ])

t(slug="teeth-replacement", name="Teeth Replacement", group="replace", video="treat", ba=["Crowns", "Veneers", "Inlay", "Overlay"],
  summary="Implants, veneers, crowns, inlays and onlays.",
  lead="Missing teeth affect more than confidence. Gum disease, genetics, injury and decay can all lead to tooth loss, and an unreplaced tooth can cause further problems. We help you choose the fixed option best suited to you.",
  sections=[
   ("Veneers", ["Thin, tooth-coloured shells, custom made in composite or ceramic, that sit over the visible surface of the front teeth to change their colour, shape and size. A less invasive way to fix discoloured, chipped, broken, slightly misaligned or irregular teeth, and the basis of most 'Hollywood smile' makeovers."], []),
   ("Inlays, onlays and overlays", ["Indirect fillings for moderate decay where a direct filling would take too long and a crown is more than you need. Made in durable materials such as metal or zirconia, they significantly strengthen the tooth. An inlay sits between the cusps on the chewing surface; an onlay covers one or more cusps."], []),
   ("Dental implants", ["The most effective, permanent replacement for one or more missing teeth, or teeth damaged beyond repair, with a high success rate. An implant can replace a single tooth, support a bridge, or hold a full prosthesis when all teeth are missing. Depending on the available bone we use conventional, basal, pterygoid or zygoma implants.",
     "In the conventional approach the tooth is removed, the implant screw placed straight away and left to integrate with the jawbone for two to three months before the crown is fitted. With immediate loading, the screw and crown are placed together. Through our Teeth in an Hour programme you can walk out with new, natural-looking teeth in one visit, and many international patients fly in for this.",
     "Our implant dentists keep discomfort to a minimum. Implant attachments can also make dentures far more secure and comfortable."], []),
  ])

t(slug="teeth-in-an-hour", name="Teeth in an Hour", group="replace", video="treat", ba=["Teeth in an hour"],
  summary="Permanent implant teeth fixed in a single visit.",
  lead="Teeth in an Hour gives patients new, permanent implant teeth in record time. Veeyes is one of very few clinics in the region offering it.",
  sections=[
   ("How it works", ["For patients with a healthy jawbone, we use 3D imaging scans and X-rays to plan the right fit in advance. On the day, implants and natural-looking restorations are fixed in about an hour, at an affordable cost."], []),
  ])

t(slug="full-mouth-rehabilitation", name="Full Mouth Rehabilitation", group="replace", video="treat", ba=["Full mouth rehabilitation"],
  summary="Rebuilding function and appearance across the whole mouth.",
  lead="Full mouth rehabilitation replaces some or all missing teeth and restores damaged ones to give the best possible function and appearance. It is called 'full mouth' because it may involve every tooth, using crowns, bridges or implant-supported teeth.",
  sections=[
   ("When it is needed", [], ["Complete loss of teeth", "Badly broken-down teeth", "Heavy staining from tobacco (external) or fluorosis (internal)", "Mal-positioned teeth, within limits", "Spacing between teeth", "Multiple teeth lost to gum disease or decay", "Loss of tooth height from wear or night grinding", "TMJ disorders"]),
   ("What the treatment involves", ["We identify the root causes, then plan and sequence treatment across several specialities: prosthodontics, endodontics, orthodontics, oral surgery, oral medicine and general dentistry.",
     "Remaining natural teeth can anchor replacements for lost ones, or support removable metal or acrylic dentures. Where no natural teeth remain, titanium implants anchored in the jawbone allow a fixed replacement of every tooth, with chewing efficiency close to natural teeth.",
     "Implants can also anchor advanced removable or fixed prostheses, giving them more stability and retention for better chewing."], []),
  ])

t(slug="restorative-dentistry", name="Restorative Dentistry", group="replace", video="treat", ba=["Front tooth filling", "Back tooth filling"],
  summary="Fillings, crowns and root canal treatment that restore function.",
  lead="Restorative dentistry rebuilds tooth surfaces lost to decay, fracture or wear. Where cosmetic dentistry focuses on appearance, restorative work focuses on oral health and function. We use the best direct and indirect fillings for each case.",
  sections=[
   ("Choosing a restoration", ["Decay starts when bacteria attack enamel; the damaged part is removed and replaced. Which material suits you depends on your oral health, the size and position of the filling, chewing load and how many visits you can make. Direct options include glass ionomer, GIC capsule and tooth-coloured composite fillings. Indirect options include inlays, onlays and overlays."], []),
   ("Composite fillings (tooth coloured)", ["Glass or quartz filler in a resin base. Durable and fracture-resistant for small and mid-sized fillings under moderate chewing pressure. Less tooth needs removing than with amalgam, and composites bond to the tooth, allowing more conservative repairs. They take a little longer to place."], []),
   ("Glass and resin ionomers", ["Tooth-coloured materials that release fluoride and need minimal preparation, suited to root-surface cavities and small fillings away from heavy chewing. They lack the translucency of enamel and can wear faster on biting surfaces. Allergies are rare."], []),
   ("Amalgam", ["Used for over a century for its durability and low cost, but it looks unnatural, can cause short-term sensitivity and needs more tooth removed. It is now considered outdated."], []),
   ("Indirect restorations (two or more visits)", ["Crowns, inlays and onlays are made in a lab from a mould. Crowns cover the whole tooth, inlays fit within it and onlays cover part or all of the chewing surface."],
    [("All-ceramic", "Colour and translucency closest to natural enamel. Strong when thick enough and well bonded, and very wear resistant."), ("Porcelain fused to metal", "Very strong and durable, but needs more tooth removed and can wear opposing teeth if the surface roughens."), ("Gold alloys", "Tough, corrosion resistant and gentle on opposing teeth, with little healthy tooth removed. They don't look like natural teeth."), ("Base metal alloys", "Strong, silver-coloured and corrosion resistant, used for crowns, bridges and partial dentures."), ("Indirect composites", "Tooth coloured and kind to opposing teeth, but less strong than porcelain or metal and more prone to wear and staining.")]),
   ("Root canal treatment and functional crowns", ["Root canal treatment saves badly decayed or infected teeth. The nerve and pulp are removed, the canals are filled with gutta-percha and sealed, and a crown protects the tooth. Signs you may need one: lingering sensitivity, pain when biting, swelling, or deep decay or injury."], []),
  ])

t(slug="biominmetic-dentistry", name="Biomimetic Dentistry", group="replace", video="treat", ba=["Inlay", "Overlay"],
  summary="Minimally invasive repairs that mimic natural teeth.",
  lead="Biomimetic dentistry repairs damaged teeth with minimally invasive techniques and materials that mimic natural tooth structure, preserving as much of your own tooth as possible.",
  sections=[
   ("Why it matters", ["Teeth restored this way look and feel like natural teeth in form and function, and the approach is affordable. Treatments are efficient, easy to tolerate and long-lasting. Veeyes has been a pioneer of biomimetic restorative dentistry in the region."], []),
   ("Inlays, onlays and overlays", ["Indirect restorations for moderate decay where a crown is more than you need. Made in durable materials such as zirconia, they strengthen the tooth significantly. An inlay sits between the cusps; an onlay covers one or more of them."], []),
  ])

t(slug="tooth-fracture-management", name="Tooth Fracture Management", group="replace", video="treat", ba=["Tooth fracture"],
  summary="Repairing chipped, cracked and split teeth.",
  lead="Teeth fracture from accidents, uneven biting forces or biting something hard. Because teeth cannot heal themselves, they need repair to keep their form and function.",
  sections=[
   ("Treatment depends on the fracture", [], [("Enamel only", "A tooth-coloured filling or a veneer is usually enough."), ("Reaching the centre of the tooth", "Root canal treatment, followed by a cap or veneer."), ("Through-and-through fracture", "The tooth is removed and replaced with an implant.")]),
  ])

t(slug="cosmetic-dentistry", name="Cosmetic Dentistry", group="cosmetic", video="whitening", ba=["Cosmetic dentistry"],
  summary="Smile makeovers, veneers, bonding and whitening.",
  lead="Cosmetic dentistry improves the look of your teeth, gums and smile. Stained, worn, discoloured, broken, misaligned or chipped teeth and gaps can all be corrected, improving the health and function of your teeth as well as their appearance.",
  sections=[
   ("What it includes", ["Ceramic and invisible braces, composite and porcelain veneers, crowns, gum treatment, composite fillings, whitening and bleaching, and dental implants. We work with you on a plan that is right for you and economical, including complete smile makeovers and pre-wedding makeovers in a short time."], []),
  ])

t(slug="smile-designing", name="Smile Designing", group="cosmetic", video="whitening", ba=["Smile designing"],
  summary="Planning shape, contour and colour for your face.",
  lead="Smile designing enhances the appearance and form of your smile by managing the shape, contour and colour of your teeth in relation to your face.",
  sections=[
   ("Procedures we combine", [], ["Composite bonding", "Teeth whitening", "Implants", "Dental laminates", "Aesthetic crowns", "Tooth replacement"]),
  ])

t(slug="teeth-whitening", name="Teeth Whitening", group="cosmetic", video="whitening", ba=[],
  summary="Home and in-clinic bleaching for a brighter shade.",
  lead="Teeth whitening is a simple, painless way to make your teeth whiter. Enamel has microscopic pores that pick up stains over time from smoking and food colouring; discolouration can also come from antibiotics or fluoride while teeth are forming.",
  sections=[
   ("Two ways to whiten", [], [("Home bleaching", "Gel in a clear custom tray that fits snugly over your teeth, worn during the day or overnight for several days to a couple of weeks. Typically lifts the shade 2 to 3 steps."), ("In-office bleaching", "Gel is applied to the front teeth and activated with laser light, in one or two visits. Typically lifts the shade 6 to 8 steps.")]),
   ("What to expect", ["Any bleaching can cause some sensitivity and gum irritation, which settles within one to three days. Results last six months to a year depending on habits such as smoking, paan chewing, coffee and tea. Every case is different, so ask us to explain the procedure and likely outcome for you, and for a cost estimate."], []),
  ])

t(slug="laser-dentistry", name="Laser Dentistry", group="cosmetic", video="treat", ba=["Laser gum treatment"],
  summary="Gentler treatment for teeth and gums with dental lasers.",
  lead="Almost every part of dental care can be improved with laser therapy, and lasers are now a mainstay of treatment for both teeth and gums.",
  sections=[
   ("Advantages", [], ["Painless, bloodless procedures and surgery", "Injections can be avoided in most cases", "No stitches", "Less need for antibiotics and painkillers afterwards", "Less swelling and discomfort", "Quicker recovery"]),
   ("What we use lasers for", [], [("Desensitising", "Reduces sensitivity across several teeth from gum recession or enamel wear."), ("Laser bleaching", "Whitening with less sensitivity than conventional methods."), ("TMJ pain", "Effective in treating jaw joint pain."), ("Cavity preparation", "No drill, so no noise or vibration, and less sensitivity afterwards."), ("Growth removal", "Painless removal of small growths in the mouth."), ("Gum de-pigmentation", "Lightening dark gums."), ("Frenectomy", "Releasing the tissue that ties the lip to the gum."), ("Curettage", "Conservative treatment of infected gums."), ("Gingivectomy", "Reducing excess gum for a gummy smile."), ("Mouth ulcers", "Disinfecting and sealing an ulcer to relieve pain."), ("Laser-assisted root canals", "The highest level of disinfection inside the canal."), ("White lesions", "Removing early, possibly pre-cancerous lesions."), ("Implant uncovering and infections", "Bloodless exposure of implants, and early treatment of infected implants to prevent failure.")]),
  ])

t(slug="teeth-management", name="Pain Management", group="everyday", video="treat", ba=[], single="Wisdom tooth removal",
  summary="Root canals, extractions and wisdom tooth removal, without the pain.",
  lead="Toothache is the most common reason people visit a dentist. Your comfort before, during and after treatment comes first. From painless local anaesthesia to aftercare, we choose the technique best suited to you.",
  sections=[
   ("Root canal treatment", ["Three in four patients who come to us with toothache need a root canal. We offer advanced endodontics, including microscopic endodontics, laser root canals and treatment under loupes for better magnification."],
    ["An opening is made in the decayed or infected tooth", "The infected pulp inside is removed and the canals decontaminated", "The canals are filled with a rubber-like material called gutta-percha", "The tooth is sealed with a filling and/or a crown to protect it"]),
   ("", ["With painless injection technique you won't feel pain during the procedure, and with the aftercare your dentist advises you can use the tooth normally again soon."], []),
   ("Tooth extraction", ["When a tooth is damaged beyond repair it may need removing. A simple extraction is used when the tooth is visible and comes out in one piece; a surgical extraction when surrounding tissue or bone must be removed. Both are done under local anaesthesia. Common reasons:"],
    ["Decay or infection beyond repair", "Gum disease", "Injury to the tooth or surrounding bone", "Wisdom tooth complications", "Crowding, or preparation for braces", "Extra (supernumerary) or retained baby teeth"]),
   ("Wisdom tooth removal", ["Wisdom teeth are the last molars to erupt, in early adulthood. Many come through partly or at an angle, and at the back of the jaw they are hard to clean, which often leads to infection of the surrounding gum (pericoronitis). Removal is one of the most common procedures in dentistry. Reasons include:"],
    ["Decay", "Repeated pericoronitis, cellulitis or abscess", "Gum disease and pus formation", "Growth at an irregular angle or alignment problems", "Removal in advance as a preventive measure"]),
  ])

t(slug="preventive-dentistry", name="Preventive Dentistry", group="everyday", video="consult", ba=[], single="Preventive dentistry",
  summary="Check-ups, cleaning, fluoride and sealants.",
  lead="Preventive dentistry helps you avoid dental problems and catch them early: cavities, gum disease, misaligned teeth and tooth loss. It matters most for children and young adults, but everyone benefits.",
  sections=[
   ("Habits and treatments we promote", [], ["Proper brushing technique to remove bacteria and plaque", "Daily flossing to clear food trapped between teeth", "Regular check-ups and cleaning", "Awareness of the effects of smoking and tobacco chewing", "Fluoride applications", "Pit and fissure sealants for children, to prevent cavities early"]),
   ("Dental camps", ["We run regular dental camps around Coimbatore and Tiruppur to teach brushing technique and detect early decay and gum disease. Many parents worried about their children's teeth have benefited."], []),
  ])

t(slug="kids-family-dentistry", name="Kids & Family Dentistry", group="everyday", video="kids", ba=[],
  summary="Teddy Teeth, our child-friendly clinic, and care for every age.",
  lead="Our child-friendly clinic, Teddy Teeth, uses toys and a gentle pace so children enjoy their visits. We offer full oral evaluations, preventive care, fluoride, sealants, crowns and more. Healthy baby teeth matter for permanent teeth, speech, nutrition and self-esteem.",
  sections=[
   ("Habits to build at home", [], ["Brush twice a day, morning and night", "Don't let children sleep with a milk bottle", "Use a toothpaste with the right amount of fluoride", "Cut down sugary foods; offer fruit, vegetables and unsweetened yoghurt", "Include calcium-rich foods such as milk, cheese and green vegetables"]),
   ("Before the visit: do", [], ["Describe it positively, as meeting a friendly doctor", "Explain that check-ups find problems early", "Bring both parents to the first visit if you can", "Give the dentist time to build rapport", "Bring medical records, including immunisations"]),
   ("Before the visit: don't", [], ["Talk about pain, blood or injections", "Mislead your child about how long treatment takes", "Use the dentist as a threat", "Push for treatment straight away", "Book during nap time or when your child is tired", "Bribe with gifts, or complain about your child during the visit"]),
   ("Family dentistry", ["We are the family dentist for many households in and around Coimbatore and Tiruppur, caring for everyone from young children to grandparents. Many patients travel from other districts and states to be treated by our chief surgeons."], []),
  ])

t(slug="geriatric-dentistry", name="Geriatric Dentistry", group="everyday", video="treat", ba=[],
  summary="BPS dentures, implants and gentle care for older patients.",
  lead="A common belief among older people is that it isn't worth fixing teeth at their age. Good teeth help you chew, which supports nutrition and general health, and general health in turn affects your mouth.",
  sections=[
   ("What we provide", ["BPS dentures, implant-retained dentures, full mouth rehabilitation with bridges, implants, crowns and removable partial dentures. We also treat sensitivity, severe wear, loose teeth (splinting), and provide cleaning and gum treatment."], []),
   ("Medically compromised patients", ["We adapt treatment for patients with diabetes, heart conditions and physical disabilities."], []),
  ])

t(slug="gum-treatment", name="Gum Treatment", group="everyday", video="consult", ba=["Gum treatment"],
  summary="Cleaning, root planing and periodontal surgery.",
  lead="Gum disease (periodontitis) is usually caused by bacteria building up from incorrect brushing and flossing. Early signs are bleeding gums, persistent bad breath, loosening teeth and receding gums. Left untreated, it leads to chewing problems and tooth loss.",
  sections=[
   ("Causes", ["As well as hygiene, hormonal changes, smoking, family history and reduced saliva flow can all contribute."], []),
   ("Treatment", ["Depending on the stage, our periodontist may recommend cleaning and root planing, periodontal surgery, bone substitutes or guided tissue regeneration (GTR), at affordable prices."], []),
  ])

t(slug="digital-dentistry", name="Digital Dentistry", group="digital", video="xray", ba=[],
  summary="CBCT, intra-oral scanning, digital smile design and CAD/CAM.",
  lead="We are one of few clinics using digital tools at every stage of dentistry, from patient records to the crown that goes in your mouth. It shortens chair time and makes treatment more comfortable.",
  sections=[
   ("What we use", [], ["Digital patient records", "RVG, OPG and lateral cephalogram imaging", "3D CBCT imaging for diagnosis", "Trios 3D intra-oral scanner for teeth and soft tissue", "Digital treatment planning and digital impressions", "Computer-aided design and milling of crowns and prostheses"]),
   ("What it means for you", ["Digital smile design lets you see the result before treatment begins. Digital impressions give a more accurate fit, so crowns last longer, and digital planning for braces predicts the outcome more precisely."], []),
  ])

t(slug="digital-radiography", name="Digital Radiography", group="digital", video="xray", ba=[],
  summary="Lower-radiation X-rays you can see straight away.",
  lead="Digital radiography captures X-ray images on a sensor instead of film and sends them straight to a computer, so your dentist can review them in real time.",
  sections=[
   ("Advantages", [], ["Less radiation", "Instant preview", "Faster appointments", "Lower cost", "Portable equipment", "Sharper, enhanced images"]),
   ("At Veeyes", ["As an implant centre, we rely on some of the most advanced and accurate diagnostic equipment in dentistry today, including 3D CBCT."], []),
  ])

T_BY = {x["slug"]: x for x in T}

# ---------------------------------------------------------------- hospital
HOSPITAL = [
 ("Operation theatre", "Dental care under general anaesthesia",
  ["Some patients cannot manage treatment in an outpatient chair. For them we provide dental care under general anaesthesia in an operating room, with its own medical, dental and hospital protocols.",
   "Our team completes a full pre-operative assessment of health and anaesthesia risk, and dentists work alongside anaesthesiologists and surgical staff throughout. Strict infection control and sterilisation apply to every procedure."]),
 ("Surgical ICU", "Monitoring after major procedures",
  ["The surgical intensive care unit is for post-operative patients who need constant monitoring and may need emergency intervention.",
   "SICU nurses have specialised critical-care training. They manage medication and vital signs, respond quickly to changes, and work closely with physicians to support safe recovery."]),
 ("NOIS sedation", "Nitrous oxide inhalation sedation",
  ["Nitrous oxide (N₂O) is the most widely used inhalation sedative in dentistry, also used in emergency rooms and day-surgery centres.",
   "On its own it doesn't give general anaesthesia, but it is very safe and gives excellent mild to moderate sedation for nervous patients and minor oral surgery."]),
 ("Sterilisation", "Five-step protocol, every room",
  ["Our trained dental assistants follow a five-step sterilisation protocol across the hospital, covering every instrument, piece of equipment, dental chair and operatory, in line with international standards."]),
]

# ---------------------------------------------------------------- blog
POSTS = [
 {"slug": "root-canal-treatment-explained", "title": "Understanding the basics of root canal treatment", "date": "7 June 2021", "read": "2 min read",
  "img": wix("d6c03a_3200f9aee8fc48f18ea3494657f3ed1f~mv2.jpg", 1400),
  "excerpt": "A root canal saves a badly decayed or infected tooth. Here's what actually happens, and how to know if you need one.",
  "body": [
   ("p", "A root canal treatment is recommended to save a badly decayed or infected tooth. The term 'root canal' refers to the hollow section of your tooth that contains nerves, blood vessels and connective tissue, known as the pulp. During the procedure the infected pulp is cleaned out, and the tooth is filled and sealed."),
   ("h", "Does root canal treatment hurt?"),
   ("p", "This is the question we hear most. The procedure itself is not painful because it is done under anaesthesia; the pain people associate with it comes from the infection. Afterwards you may feel a little sore or numb, with mild tenderness for a few days."),
   ("h", "What happens, step by step"),
   ("ol", [("Numbing the tooth", "Local anaesthesia is given. A thin rubber sheet called a dental dam isolates the tooth and keeps it clean and dry."), ("Cleaning the tooth", "A small opening is made in the top of the tooth and fine files remove the infected pulp. The canals are rinsed and an antimicrobial solution reduces the risk of further infection."), ("Closing the tooth", "The tooth is filled and closed with a crown or similar restoration. Until then, avoid chewing on that side.")]),
   ("h", "How do you know if you need one?"),
   ("p", "Root canals are needed when a cavity reaches the pulp, after an injury, or sometimes because of problems with an earlier filling. Signs to look out for:"),
   ("ul", ["Sensitivity to hot or cold that lingers after you've finished eating or drinking", "Pain when chewing or biting, or for no clear reason", "Pimples on the gums, or swollen, tender or darkened gums"]),
   ("p", "Visit your dentist regularly for cleaning and a general check-up."),
  ]},
 {"slug": "a-basic-guide-to-your-child-s-dental-hygiene", "title": "Teaching your child good dental hygiene habits", "date": "7 June 2021", "read": "2 min read",
  "img": wix("d6c03a_9ce3c1350a454114add3bbf9340a2f46~mv2.jpg", 1400),
  "excerpt": "From a baby's first tooth to the school years: a practical guide for parents.",
  "body": [
   ("p", "Children's dental habits are often overlooked until there's a problem, and good information can be hard to find. Here is a simple guide for parents."),
   ("h", "Infants"),
   ("ul", ["Good care starts before the first tooth. Wipe your baby's gums with a clean, damp cloth to clear away bacteria.", "Once teeth appear, brush twice a day with an infant toothbrush and a grain-sized smear of fluoride toothpaste.", "Plan the first dental visit before the first birthday, or within six months of the first tooth.", "Avoid 'baby bottle decay': don't put your baby to sleep with juice, formula or milk. Sugary liquids cling to teeth and feed decay-causing bacteria."]),
   ("h", "Toddlers"),
   ("ul", ["From about two, encourage children to brush their own teeth with a pea-sized amount of fluoride toothpaste, and make sure they don't swallow it.", "Teach flossing early. For children with braces, a powered toothbrush helps.", "Watch for bite problems as teeth come in: crowding, underbite, overbite or protruding teeth. Book check-ups every six months."]),
   ("h", "Make it a habit"),
   ("p", "Poor habits in childhood lead to decay and cavities in adult teeth, and can reduce the space adult teeth need. Ask your dentist about pit and fissure sealants to prevent cavities."),
   ("p", "Let children choose their own toothbrush and fluoride toothpaste. Rather than just supervising, brush with them so it becomes something to look forward to. Keep an eye on diet too: sweets, juice and starchy snacks are hard on growing teeth."),
  ]},
 {"slug": "6-warning-signs-it-s-time-for-your-dental-check-up", "title": "Six signs you're overdue for a dental check-up", "date": "7 June 2021", "read": "3 min read",
  "img": wix("d6c03a_d49105f91c2241058466756df1158400~mv2.jpeg", 1400),
  "excerpt": "Bleeding gums, sensitivity, sores that won't heal. When to stop putting off your appointment.",
  "body": [
   ("p", "Not everyone sees a dentist regularly, but check-ups catch problems early, before they become emergencies, and help prevent deep decay, severe bite problems and gingivitis. If you've been putting it off, here are six signs it's time."),
   ("ol", [("Bleeding when brushing, flossing or eating", "Blood on your toothbrush isn't normal. It can be a sign of gum disease, an infection of the tissues that hold your teeth. Untreated, it can lead to bone loss and eventually tooth loss."), ("Toothache or gum ache", "Don't ignore it, even if it fades after a day. It could be a cavity, abscess, broken tooth, damaged filling or grinding. Only your dentist can find the cause."), ("Sensitivity to hot or cold", "Sudden sensitivity can mean a cavity or weakened enamel. You should be able to enjoy hot and cold food without pain."), ("Sores in the mouth", "If a sore lasts more than a week, see a dentist. Thrush (candidiasis), a fungal infection, can appear as white patches on the tongue, cheeks, tonsils or palate."), ("Bad breath", "Occasional bad breath is normal. If it lasts several days despite good hygiene, it may point to an underlying problem or a cleaning that's overdue."), ("Loose or discoloured teeth", "Injury, osteoporosis and other causes can loosen teeth, and implants can loosen too. Brown marks that don't brush off, or small white spots, can be early signs of decay.")]),
   ("p", "Dental health and general health are more closely linked than most people realise. Keep up with check-ups twice a year, and see your dentist sooner if you notice any of the signs above."),
  ]},
 {"slug": "dental-cavities", "title": "The hidden dangers of neglecting cavities", "date": "7 June 2021", "read": "2 min read",
  "img": wix("d6c03a_fb72d65675ef487aa08fa27966b7464c~mv2.jpg", 1400),
  "excerpt": "Chocolate isn't the only culprit. What causes cavities, how to spot them, and how they're treated.",
  "body": [
   ("p", "We were all told as children that chocolate rots your teeth. The truth is that many factors cause cavities, and the acid produced by bacteria is as much to blame as sugar."),
   ("p", "Cavities form when tooth enamel breaks down. Bacteria feed on sugary and acidic food, and without good hygiene and prevention the result is usually decay."),
   ("h", "Common causes"),
   ("ul", [("Eating habits", "Frequent snacking on sugary and acidic foods."), ("Position of the teeth", "Molars and premolars at the back are harder to clean."), ("Saliva flow", "Saliva washes away food and plaque and helps neutralise acid, so a dry mouth raises the risk."), ("Hygiene", "Inadequate brushing and not cleaning soon after eating or drinking.")]),
   ("h", "Symptoms"),
   ("p", "Early cavities often have no symptoms. Over time you may notice:"),
   ("ul", ["Black, brown or white staining on a tooth", "Pain or sensitivity with hot or cold, or with no obvious cause", "Visible holes in the tooth surface", "Swelling, in severe cases"]),
   ("h", "Treatment"),
   ("p", "Treatment depends on how far the decay has gone: a tooth-coloured filling, root canal treatment if the decay has reached the pulp, or extraction if the tooth can't be saved."),
   ("h", "Prevention"),
   ("ul", ["Brush and floss thoroughly and regularly", "Use a fluoride toothpaste or mouth rinse, and ask about sealants for back teeth", "See your dentist regularly for cleaning and check-ups", "Make sure no food stays stuck in the grooves of your teeth"]),
  ]},
]
