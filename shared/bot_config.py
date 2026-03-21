import discord

server_id = 117664143837888519



owner_id = 87493043594207232 # Night
bot_lord = 297368243985711105 # Luna
testing_account = 00000000000000000

fez_id = 168150049023459328
transbot_id = 208059113559556097
pasta_id = 1140813542929465444
minecraft_bridge_id = 1200698054047699045
test_bot_id = 1213522036002131978

# Plural Kit
pk_id = 466378653216014359
pk_webhook = 625448416528433184

wl_ico = ':children_crossing: '
channel_length = 25

emojis = {
    'logo': '<:logo:230183723176296449>',
    'fez': '<:fez:1082554012169146378>',
    'fezcool': '<:fezcool:585838797439238165>',
    'fezhappy': '<:fezhappy:585838797384843294>'
}

# ordered by channel.position
ch_id = {
    '#info': 1179263124948385913,
    '#faq': 961734773502537809,
    '#announcements': 119368839895973888,
    '#action-log': 1097958530612465704,
    '#general': 126496396005212160,
    '#general-two': 215642551003119616,
    '#trans-masc': 149143053494386688,
    '#nonbinary': 149145241839075328,
    '#trans-fem': 149143570228445184,
    '#set-topic-light': 513795424801259524,
    '#set-topic': 159807561690906634,
    '#set-topic-serious': 346428202459201537,
    '#server-help': 606550086360760340,
    '#random': 121419182658027522,
    '#bot-spam': 413114858029056030,
    '#fezboard': 434866717202710529,
    '#event-text': 186251878370246657,
    '#transition-questions': 491978339112845312,
    '#transition-trans-masc': 353686647730208778,
    '#transition-nonbinary': 353686900772438016,
    '#transition-trans-fem': 353686257856937994,
    '#politics': 1303958634220228699,
    '#mental-physical-health': 123975995450589184,
    '#relationships': 163448187577696256,
    '#food': 530267206798540800,
    '#gaming-club': 119353107107938304,
    '#media-club': 124536589060669443,
    '#venting-chat': 1325964322446377051,
    '#venting-chat-two': 1325964689590456400,
    '#venting-no-replies': 1325965058978746508,
    '#support-one': 1325961184041504861,
    '#support-two': 1325962612026118194,
    '#support-three': 1325961707645964288,
    '#support-four': 1325962106088063006,
    '#support-verified': 1325963071981621410,
    '#safe-support': 1325963473884024842,
    '#entry-info': 314041247721586690,
    '#landing-room': 117664143837888519,
    '#entry-reg': 314041198417281025,
    '#dm-reminders': 1398238875746566174,
    '#staff-starboard': 383363070992449539,
    '#staff-politics': 246015920793714688,
    '#staff-moderation': 834851053227868160,
    '#nsfw-discussion': 737089888645677137,
    '#staff-mod-logs': 725059393556709436,
    '#staff-trigger-words': 538592790897229834,
    '#staff-no-no-words': 369929422817591297,
    '#staff-on-leave': 326411103967903754,
    '#staff-announcements': 141546588341403648,
    '#bot-dev': 447143789186908170,
    '#fez-gym': 254353561088032768,
    '#unified-chat-sfw': 382639554194046986,
    '#unified-chat-nsfw': 123998091551440897,
    '#unified-chat-staff': 575959770725613569,
    '#bot-dms': 480767730799214592,
    '#event-planning': 234810311872348170,
    '#bans-warnings': 126783168429817856,
    '#staff-warnings': 427552223132647425,
    '#admin-chat': 511314708238827520,
    '#staff-break-room': 680273080253546514,
    '#break-room': 680273080253546514,
    '#admin-chat-11-2018': 292074966172827649,
    '#staff-random': 922993177483423804,
    '#staff-off-my-chest': 950326952756150282,
    '#lead-chat': 1190224206978359357,
    '#staff-discussion': 737089778717032489,
    '#staff-discussion-two': 737089808756768791,
    '#staff-discussion-three': 1141937830881402930,
    '#staff-orientation': 896813370773209139,
}

BASE_URL = f'https://discord.com/channels/{server_id}'
channel_url = {}
for channel, id in ch_id.items():
    channel_url[channel] = f'{BASE_URL}/{id}'

nono_disable = (
    'plurality',
    'poc',
    'holiday-sentiments'
)

trigger_disable = (
    'support-one',
    'support-two',
    'support-three',
    'support-four',
    'support-five',
    'neurodivergent',
    'mental-physical-health',
    'venting-chat',
    'venting-no-replies',
    'venting-chat-two',
    'relationships',
    'holiday-sentiments',
    'poc',
    'plurality'
)

topic_channels = (
    ch_id['#set-topic'],
    ch_id['#set-topic-serious'],
    ch_id['#set-topic-light'],
)

milestone_disable_channels = (
    ch_id['#support-one'],
    ch_id['#support-two'],
    ch_id['#support-three'],
    ch_id['#support-four'],
    ch_id['#support-verified'],
    ch_id['#safe-support'],
    ch_id['#venting-no-replies'],
    ch_id['#venting-chat'],
    ch_id['#venting-chat-two'],
    ch_id['#relationships'],
    ch_id['#mental-physical-health'],
)

ignored_channels = (
    ch_id['#admin-chat'],
    ch_id['#announcements'],
    ch_id['#bans-warnings'],
    ch_id['#event-planning'],
    ch_id['#info'],
    ch_id['#staff-announcements'],
    ch_id['#staff-break-room'],
    ch_id['#staff-mod-logs'],
    ch_id['#unified-chat-nsfw'],
    ch_id['#unified-chat-sfw'],
    ch_id['#unified-chat-staff'],
    ch_id['#staff-orientation'],
    ch_id['#nsfw-discussion'],
    ch_id['#staff-discussion'],
    ch_id['#staff-discussion-two'],
    ch_id['#staff-moderation'],
    ch_id['#politics'],
    ch_id['#staff-random'],
    ch_id['#staff-no-no-words'],
    ch_id['#lead-chat'],
    ch_id['#staff-off-my-chest'],
    ch_id['#staff-on-leave'],
    ch_id['#staff-starboard'],
)

vc_id = {
    'AFK': 119354402770255873,
    'Event Voice': 206199284528316416,
    'General': 131781833376399360,
    'General 2': 119354655279939584,
    'General Verified': 287348004581670912,
    'Voice-Training': 117874045583753217,
    'Trans Masc': 149145435263467520,
    'Trans Fem': 149145421560807424,
    'Nonbinary': 149145460878082048,
    'Game Room': 119354617350848514,
    'Music Bot': 267904080440066048,
    'Music 2': 547601580502024218,
    'Staff Chat': 133518666128949248,
}

# ordered by role.position
rl_id = {
    'owner': 257362700835880961,
    'founder': 257362700835880961,
    '*': 996603692826509402,
    'admin': 117873055362973702,
    'lead-mod': 205878396763373568,
    '-': 1478827005087711414,
    'mod': 117872710670876674,
    'in-training': 259938392962236417,
    'on-leave': 424672058387988491,
    'a-director': 486993366232596491,
    'bot': 119600635158069249,
    'helper': 1412037916917764117,
    'staff': 175786985430974465,
    'staff-junior': 1387323414150119444,
    'staff-alert': 295418997871214592,
    'bot-administrator': 388479117210943489,
    'event-director': 291706269822222336,
    'event-coord': 234618811532181504,
    'partner': 444374792414429226,
    'regular': 117873225135947781,
    'new': 215589946218643457,
    'musicbot': 267884724725350400,
    'ae': 789703319198367754,
    'xey': 843138911202836530,
    'it': 452308189036150804,
    'fae': 472774190903328778,
    'ey': 491810908507602956,
    've': 843138738980782081,
    'ne': 911448562863325204,
    'shi': 1208538507673600030,
    'ask-pronouns': 538562048913702912,
    'no-pronouns': 639609854985764884,
    'switch-pronouns': 579561477086773248,
    'mirrored-pronouns': 1043983647256100925,
    'not-he': 483331758046052372,
    'not-she': 483331841923874826,
    'not-they': 508496598309797908,
    'ask-gender': 789703360897875989,
    'nonbinary': 123539518786633729,
    'agender': 155389338341867520,
    'aporagender': 555881382933561375,
    'bigender': 276730351559114764,
    'trigender': 843144702949589002,
    'polygender': 843139138189918270,
    'boyflux': 789703412392132679,
    'demigender': 277173431114530816,
    'pangender': 911448518017843211,
    'paragender': 843139267345252352,
    'demiboy': 314473273972752385,
    'demigirl': 314471400322629632,
    'demiflux': 508497232811655179,
    'fluidflux': 639609836560056352,
    'genderfae': 789702697892053023,
    'genderfaun': 789702866267799602,
    'genderflor': 843139424241975326,
    'genderfluid': 123084880421584897,
    'genderflux': 314473318818512898,
    'gendernull': 911448620212056065,
    'genderqueer': 144656645987762177,
    'gender-neutral': 1209524956040532061,
    'gendervoid': 526799020434259979,
    'girlflux': 789703427953000448,
    'libragender': 606344542664261632,
    'neutrois': 483453240739102730,
    'intersex': 290638267018379276,
    'two-spirit': 508497422549385246,
    'mtf': 149182721997012992,
    'ftf': 592591941812617226,
    'ftm': 149182738170249216,
    'mtm': 592591950696415242,
    'ftnb': 508496874689396736,
    'mtnb': 508497062715850772,
    'nbtnb': 600445967254159449,
    'trans': 606344556266520577,
    'trans-androgynous': 606344524528222210,
    'trans-feminine': 290638105600458754,
    'trans-neutral': 483331488641712138,
    'trans-masculine': 290638004995883008,
    'trans-man': 300762444731514880,
    'trans-boy': 314473390398504962,
    'trans-male': 526527254931439626,
    'trans-female': 526527284111212545,
    'trans-girl': 314473353941483520,
    'trans-woman': 300762406307627008,
    'transsexual-woman': 300761981940531200,
    'transsexual-man': 300762112219676676,
    'transsexual-girl': 336692100382851073,
    'transsexual': 1194539619006558268,
    'xenogender': 789703389134848030,
    'boy': 1043978997672972339,
    'girl': 1043979010343977011,
    'boygirl': 1200118561516036166,
    'man': 1099431164676153466,
    'woman': 1099431360806015076,
    'afab': 388893872127737867,
    'amab': 395652766451761154,
    'gnc': 789703449653674034,
    "queer": 1200117826548142170,
    'masc-aligned': 813621389630111754,
    'fem-aligned': 813621580071436328,
    'butch': 1263571695000752148,
    'futch': 1272790406232412201,
    'galactian-alignment': 911448697936703488,
    'voidpunk': 1008499844664545320,
    'autigender': 1301288060004073494,
    'namefluid': 1122915745031016560,
    'cis-female': 317457689892356097,
    'cis-male': 317457882062913536,
    'detransitioner': 1138099881697882222,
    'tm-access': 526531060658339851,
    'tf-access': 526531046699958302,
    'nb-access': 526531084268208128,
    'over18': 123986718566121474,
    'event': 328633922688647179,
    '#adulting': 697260750690844763,
    '#education': 1221985115446575237,
    '#automotive': 1221985692805107812,
    '#cosmetics': 1440385722354765915,
    '#poc': 745833453853081731,
    '#politics': 1303961552352706611,
    '#covid-19': 693209815908090077,
    '#fashion': 1440384769023021106,
    '#furry': 592846911095046174,
    '#gaming': 288863219412369410,
    '#neurodivergent': 416803492775067649,
    '#non-speaking': 1221985936167141477,
    '#alterhuman': 1043986584787234920,
    '#passing-advice': 1325967245767086090,
    '#pets-animals-nature': 739517524500021359,
    '#physical-disabilities': 923444088647344129,
    '#plurality': 579565691510718514,
    '#plus-size': 923444107341348876,
    '#selfies': 1325967148845371443,
    '#stem': 346426939650736151,
    'readrules': 261749129942663169,
    'interview': 319648452164452353,
    'ignore-messages': 399284532030865418,
    'ignore-stars': 434935726434418689,
    '#philosophy': 1397923706801754132,
    '#sports-fitness': 1377319508158578768,
    'streamer': 1099545190227771504,
}


reg_rl_id = {
    'genderfluid': 123084880421584897,
    'ze': 178287656252342274,
    'xe': 293495668339900416,
    'questioning': 119364714781212674,
    'androgyne': 381488902369968128,
    'trans-feminine': 290638105600458754,
    'demigender': 277173431114530816,
    'transsexual-woman': 300761981940531200,
    'cis-female': 317457689892356097,
    'mtf': 149182721997012992,
    'cis-male': 317457882062913536,
    'demigirl': 314471400322629632,
    'trans-girl': 314473353941483520,
    'nonbinary': 123539518786633729,
    'genderflux': 314473318818512898,
    'transsexual-man': 300762112219676676,
    'trans-guy': 390245807481290783,
    'bigender': 276730351559114764,
    'ftm': 149182738170249216,
    'female': 119364439244800000,
    'amab': 395652766451761154,
    'demiboy': 314473273972752385,
    'agender': 155389338341867520,
    'trans-masculine': 290638004995883008,
    'any-pronoun': 293496037178343434,
    'trans-man': 300762444731514880,
    'afab': 388893872127737867,
    'she': 123586900337491968,
    'trans-woman': 300762406307627008,
    'he': 123586832549150720,
    'trans-boy': 314473390398504962,
    'male': 119364552403058688,
    'they': 123587145486172160,
    'genderqueer': 144656645987762177,
    'transsexual-girl': 336692100382851073,
    'intersex': 290638267018379276,
    'it': 452308189036150804,
    'fae': 472774190903328778,
    'neutrois': 483453240739102730,
    'not-he': 483331758046052372,
    'not-she': 483331841923874826,
    'trans-neutral': 483331488641712138,
    'ey': 491810908507602956,
    'not-they': 508496598309797908,
    'mtnb': 508497062715850772,
    'ftnb': 508496874689396736,
    'demiflux': 508497232811655179,
    'trans-male': 526527254931439626,
    'trans-female': 526527284111212545,
    'gendervoid': 526799020434259979,
    'ask-pronouns': 538562048913702912,
    'aporagender': 555881382933561375,
    'switch-pronouns': 579561477086773248,
    'ftf': 592591941812617226,
    'mtm': 592591950696415242,
    'nbtnb': 600445967254159449,
    'trans-androgynous': 606344524528222210,
    'libragender': 606344542664261632,
    'trans': 606344556266520577,
    'fluidflux': 639609836560056352,
    'no-pronouns': 639609854985764884,
    'gnc': 789703449653674034,
    'ae': 789703319198367754,
    'boyflux': 789703412392132679,
    'girlflux': 789703427953000448,
    'xenogender': 789703389134848030,
    'genderfae': 789702697892053023,
    'genderfaun': 789702866267799602,
    'ask-gender': 789703360897875989,
    'masc-aligned': 813621389630111754,
    'fem-aligned': 813621580071436328,
    'genderflor': 843139424241975326,
    'paragender': 843139267345252352,
    'polygender': 843139138189918270,
    'trigender': 843144702949589002,
    've': 843138738980782081,
    'xey': 843138911202836530,
    'pangender': 911448518017843211,
    'ne': 911448562863325204,
    'gendernull': 911448620212056065,
    'galactian-alignment': 911448697936703488,
    'voidpunk': 1008499844664545320,
    'undisclosed': 176823059725025281,
    'unlabeled': 1387519150775078932,
    'two-spirit': 508497422549385246,
    'boy': 1043978997672972339,
    'girl': 1043979010343977011,
    'mirrored-pronouns': 1043983647256100925,
    'man': 1099431164676153466,
    'woman': 1099431360806015076,
    'namefluid': 1122915745031016560,
    'queer': 1200117826548142170,
    'boygirl': 1200118561516036166,
    'detransitioner': 1138099881697882222,
    'shi': 1208538507673600030,
    'gender-neutral': 1209524956040532061,
    'transsexual': 1194539619006558268,
    'butch': 1263571695000752148,
    'futch': 1272790406232412201,
    'autigender': 1301288060004073494,

}

star_override = {
    'general-nonbinary': '4',
    'transition-nonbinary': '4',
    'general-trans-masc': '4',
    'transition-trans-masc': '4',
    'general-trans-fem': '4',
    'transition-trans-fem': '4',
    'test': '1',
    'general': '4',
}

mtf_chan_name = ('general-trans-fem', 'transition-trans-fem')
ftm_chan_name = ('general-trans-masc', 'transition-trans-masc')
nb_chan_name = ('general-nonbinary', 'transition-nonbinary')

ignore_msgcount = (
    ch_id['#landing-room'],
    ch_id['#random'],
    ch_id['#staff-break-room'],
    ch_id['#staff-discussion'],
    ch_id['#staff-discussion-two'],
    ch_id['#staff-orientation'],
    ch_id['#admin-chat'],
    ch_id['#staff-announcements'],
    ch_id['#bot-dev'],
    ch_id['#fez-gym'],
    ch_id['#politics'],
    ch_id['#entry-reg'],
    ch_id['#staff-random'],
    ch_id['#lead-chat'],
    ch_id['#staff-off-my-chest'],
    ch_id['#staff-on-leave'],
    ch_id['#bot-spam'],
    ch_id['#venting-no-replies']
)


info_msgids = {
    'rules1': 1434586874042646608,
    'rules2': 1434587046944706611,
    'rules3': 1434587274053423255,
    'rules4': 1434587445524959423,
    'voice_rules': 1434587612689076364,
    'procedures1': 1434587785033023621,
    'procedures2': 1434587910644170953,
    'faq_commands1': 1434588866853077023,
    'minecraft': 1434589039662469243,
    'reporting': 1434589793194606815
    # 'links1': 430617273850396674,
    # 'extra1': 430617278283776000,
    # 'extra2': 430617282293661696,
    # 'extra3': 430617285934186498,
    # 'extra4': 430617442339913728
}

entryinfo_msgids = {
    'rules1': 430624574846009344,
    'rules2': 430624611491905537,
    'rules3': 430624615178567680,
    'procedures1': 430624618869686272,
    'faq_commands1': 430624623206596610,
    'links1': 430624627929251850,
    'extra1': 430624640818216960,
    'extra2': 430624647285964800,
    'extra3': 430624652369330186,
    'extra4': 430625624651202561
}

# The version of the identity list that gets sent to new users
identities = {
    'transfemale': [
            'mtf', 'trans-female', 'trans-feminine', 'transsexual-woman',
            'trans-woman', 'trans-girl', 'transsexual-girl'
        ],
    'transfemale_pronouns': [
            'she',
        ],
    'female': [
            'female',
            'girl',
            'woman',
        ],
    'transmale': [
            'ftm', 'trans-male', 'trans-masculine', 'transsexual-man',
            'trans-man', 'trans-boy', 'trans-guy'
        ],
    'transmale_pronouns': [
            'he',
        ],
    'male': [
            'male', 'boy', 'man',
        ],
    'nonbinary': [
            'nonbinary', 'agender', 'demigender', 'bigender', 'genderfluid',
            'genderqueer', 'genderflux', 'demigirl', 'demiboy', 'androgyne',
            'trans-neutral', 'neutrois', 'ftnb', 'mtnb', 'demiflux', 'gendervoid',
            'aporagender', 'trans-androgynous', 'libragender', 'fluidflux', 'boyflux',
            'girlflux', 'xenogender', 'genderfae', 'genderfaun', 'genderflor', 'paragender',
            'polygender', 'trigender', 'pangender', 'gendernull', 'gender-neutral', 'autigender',
            'boygirl',
        ],
    'nonbinary_pronouns': [
            'ze', 'xe', 'they', 'it', 'fae', 'ey', 'ae', 've', 'xey', 'ne', 'shi',
            'any-pronoun', 'ask-pronouns', 'switch-pronouns', 'no-pronouns', 'mirrored-pronouns'
        ],
    'cis': [
            'cis-female', 'cis-male'
        ],
    'other': [
            'questioning', 'amab', 'afab', 'intersex', 'gnc', 'masc-aligned', 'fem-aligned', 'voidpunk', 'namefluid', 'butch', 'futch', 'queer'
        ]
}

# The version of the identity list that gets sent when users run the !identities command
identities_for_cmd = {
    'transfemale': [
            'mtf', 'trans-female', 'trans-feminine', 'transsexual-woman',
            'trans-woman', 'trans-girl', 'transsexual-girl', 'ftf'
        ],
    'transfemale_pronouns': [
            'she',
        ],
    'female': [
            'female',
            'girl',
            'woman',
        ],
    'transmale': [
            'ftm', 'trans-male', 'trans-masculine', 'transsexual-man',
            'trans-man', 'trans-boy', 'trans-guy', 'mtm'
        ],
    'transmale_pronouns': [
            'he',
        ],
    'male': [
            'male', 'boy', 'man',
        ],
    'nonbinary': [
            'nonbinary', 'agender', 'demigender', 'bigender', 'genderfluid',
            'genderqueer', 'genderflux', 'demigirl', 'demiboy', 'androgyne',
            'trans-neutral', 'neutrois', 'ftnb', 'mtnb', 'demiflux', 'gendervoid',
            'aporagender', 'trans-androgynous', 'libragender', 'fluidflux', 'boyflux',
            'girlflux', 'xenogender', 'genderfae', 'genderfaun', 'genderflor', 'paragender',
            'polygender', 'trigender', 'pangender', 'gendernull', 'gender-neutral', 'autigender',
            'boygirl', 'nbtnb'
        ],
    'nonbinary_pronouns': [
            'ze', 'xe', 'they', 'it', 'fae', 'ey', 'ae', 've', 'xey', 'ne', 'shi',
            'any-pronoun', 'ask-pronouns', 'switch-pronouns', 'no-pronouns', 'mirrored-pronouns'
        ],
    'cis': [
            'cis-female', 'cis-male'
        ],
    'other': [
            'questioning', 'amab', 'afab', 'intersex', 'gnc', 'masc-aligned', 'fem-aligned',
            'voidpunk', 'namefluid', 'butch', 'futch', 'queer', 'ask-gender', 'trans', 'two-spirit',
            'undisclosed', 'queer', 'detransitioner', 'transsexual', 'unlabeled'
        ]
}

opt_channels = [
    'passing-advice',
    'selfies',
    'neurodivergent',
    'fashion',
    'cosmetics',
    'automotive',
    'gaming',
    'stem',
    'plurality',
    'furry',
    'politics',
    'covid-19',
    'adulting',
    'education',
    'pets-animals-nature',
    'physical-disabilities',
    'non-speaking',
    'alterhuman',
    'philosophy',
    'sports-fitness',
]
