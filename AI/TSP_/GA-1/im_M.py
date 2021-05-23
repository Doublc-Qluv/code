import random
import numpy as np
import operator
import matplotlib.pyplot as plt

x=[]
for i in range(300):
    x.append(i)
f1=[11.523557803599253, 11.8328044549179, 12.025638598448179, 12.7224518671973, 12.869907852259018, 12.912005809363492, 12.651555627941441, 12.796959670071701, 13.192482260048962, 13.056582708457508, 12.659374736744681, 13.19165609428309, 13.391548521082623, 13.012134576574566, 13.198119777246532, 14.474366544747914, 14.117752887465331, 14.196747143000097, 14.540908397252178, 15.119753148159678, 12.919978281260725, 15.301068932799819, 14.691792130282311, 12.510137404736652, 15.059403957814363, 15.184090327564164, 14.680765806612062, 15.498131949677566, 15.507631408671218, 15.588170243308776, 15.373148110939384, 15.265584240667577, 15.249759079637402, 14.268215532185474, 15.050396225174181, 15.356223487031675, 15.279834196476566, 14.70675446991309, 15.139742780777524, 14.948562169286333, 14.974574265262984, 14.967673793058236, 15.617003718749402, 14.649357950083987, 14.575531590228737, 15.379388398290034, 15.537155696882117, 16.239863889674609, 14.971446901861407, 16.276166697601383, 16.160441568580129, 16.37143069648921, 15.694107850944714, 15.776699409044966, 16.261080456795426, 16.0741614844551, 16.148533855671328, 16.566178399905187, 15.343563535303614, 16.522740442703075, 15.636283971011039, 15.999345512946149, 15.786954102117441, 16.390192224227729, 16.055295507092609, 15.852131504806202, 16.140578250790409, 16.25785715439083, 16.654490351101302, 16.733381322536442, 15.888583637515772, 15.85916954090515, 15.609820657516469, 15.499734686783929, 16.083957250161063, 15.85040960680438, 15.934415372670482, 16.311960063609476, 15.206105763129514, 15.441441051390019, 16.098880002162282, 15.655426059100968, 15.852619406512279, 15.946535538577626, 15.020723739243133, 15.798884499996054, 16.263992076101129, 16.711238937812475, 15.62360571475079, 16.219058918868235, 15.702650366041958, 16.449289414154414, 16.375330913131091, 16.065128844922448, 16.665073668027386, 16.538601714538185, 15.02057676762527, 15.332103719485554, 15.889473716503314, 15.604724496774663, 15.144095769996097, 16.32263271469516, 15.743348543420064, 14.890466815502991, 15.656267373323798, 16.619416320594802, 16.178123736584578, 15.794468341145741, 16.851706351614485, 16.534955535656145, 14.945965433382511, 16.230719869257815, 14.221335905097705, 16.621805831513189, 15.574846079970804, 15.824220826529599, 14.772038189359687, 14.567632522607296, 14.744360097685362, 16.39327877019862, 14.635496784744282, 16.055495472039304, 16.097827902614192, 15.060683353529425, 15.071266461173147, 14.532233084336568, 16.355698753673202, 16.602002652795235, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897, 16.622875041054897]
f2=[11.451913114563499, 11.580221262874732, 11.538552420852866, 11.791484987231792, 12.105510428532346, 12.776406425530677, 12.736588636396446, 13.435906518340962, 13.217008577132287, 13.652015846364366, 13.150236629736183, 12.298858116685386, 13.7444059774731, 13.904673706583896, 14.141120069641042, 14.371704420298295, 14.102461942485613, 14.236002587556586, 13.790837394502008, 13.808060671183121, 14.791638114668711, 14.381129668248173, 14.436643282799627, 14.907190272245639, 14.981022575994213, 14.963207255270667, 15.242171374231921, 14.760670199985254, 16.453549294703656, 15.974417692565137, 15.679840823243484, 16.315025715054638, 15.682699696567274, 15.609978892681196, 16.906002436843565, 18.07810185587779, 16.453783414921077, 17.519432370804324, 15.733871676431272, 17.560907003284946, 17.971423933013988, 15.002589214470154, 16.792781938705442, 16.131726836475938, 17.092916583011725, 16.651136839471391, 16.097850196837339, 17.809439579191334, 16.138925099539254, 16.7318955568273, 18.029860750491281, 13.923165667465831, 15.812222232526869, 15.597432254201651, 16.152765234599656, 18.083017328761819, 17.137049142865997, 17.868295049652968, 17.407440028716966, 18.80796786778776, 16.893647615820257, 17.104519540904032, 17.514162318161329, 17.284890768192298, 18.294995681291759, 16.151361158756462, 16.641259315762611, 16.0916189475459, 18.868017527988087, 18.533576615409402, 14.995819148770085, 16.657765675380666, 16.039749687867989, 17.824660141569279, 17.606315187130321, 17.920147052368133, 17.676652407105916, 16.550543528276247, 17.195917294987726, 16.184316451691974, 16.302453457614675, 16.272236224258478, 16.580382890096278, 16.95114671090159, 17.977432140228849, 17.579378112345193, 15.525721870965308, 16.620037627905127, 17.235617182141084, 16.682295748242716, 17.221554991495392, 17.981810864947967, 15.182637964398046, 16.457380907027481, 17.1584480491214, 17.534583732203167, 16.11869056721174, 17.049466798832494, 17.984527133915819, 16.064189491437421, 17.930474070342701, 15.622770958695783, 16.882912764833872, 16.60969725333354, 16.536018133733183, 16.9419547041113, 16.833670105862495, 16.82263773799955, 16.9610906550901, 17.274463146475988, 16.610238334732301, 17.066631084685362, 16.13492681416367, 16.590741347088599, 16.772326910134655, 16.72077254808098, 16.955220387311794, 16.285117545701485, 16.994221657185943, 17.491597575833239, 17.728426437134981, 15.558215913909876, 15.393732375557446, 16.020973180932437, 17.270139578933982, 17.31707124088722, 16.029596908314328, 17.201922296251279, 16.879094543677347, 16.015837686638655, 17.225075229641902, 17.449691994862707, 15.961460396127315, 17.559347229554067, 17.457696426638137, 16.840418920341989, 16.854814852163756, 17.32231829745151, 17.069374299836785, 18.633613566271052, 16.790975770922152, 18.501423457177879, 19.034979547279029, 15.794329842651994, 18.491622573379811, 16.014292271675512, 16.777582415547805, 19.040744461560081, 15.906774780089261, 14.600163617373168, 15.379249058124994, 15.588947338658397, 16.887130639950026, 15.612247147606555, 15.309734166158107, 15.484570165951288, 16.152451654599446, 16.836797823623371, 16.744512833381872, 16.733183388627637, 16.491572578286675, 16.838627741413845, 16.476787713857366, 16.854656438757274, 16.7794101059642, 16.792955489143122, 17.083660538120458, 16.285393670737406, 16.934250219775244, 17.060686957803263, 17.536043131279758, 17.223281918566723, 15.575407956345128, 17.559347229554064, 15.687040409436831, 15.999317644849711, 16.698137806890653, 16.614397386927031, 16.935833340456931, 16.684490409382928, 17.913251041302146, 15.247965992693747, 16.460618111283978, 16.019304714943058, 17.08486918702053, 17.331439963091604, 16.681121095263748, 17.787825862544103, 18.22681398819725, 17.20550976595371, 18.916717789148208, 17.819984162138557, 16.774762634210873, 14.659294496438578, 16.779462269772427, 18.338324794540792, 18.768890591484684, 15.023878890159159, 15.355949249176838, 15.166320931698197, 16.142777096554777, 16.029796777787443, 17.19931698451084, 15.696525010203581, 16.974415898915044, 17.251375205536188, 16.079043737777141, 16.059876171778939, 16.695740704535812, 17.289833391873785, 16.842475482030817, 17.271060988295726, 17.72570969221626, 16.200625036113031, 17.221187580479626, 17.251375205536188, 15.782781198681409, 16.524882142722507, 16.758440703260703, 17.850538451923125, 17.36186158265793, 18.352239166955293, 18.571733229781866, 14.795971623696694, 17.531575606277396, 14.925383452232939, 17.755741973123342, 17.569689577137282, 16.788861540895532, 17.830816062892158, 15.369348707791289, 14.938413665235732, 15.223297748313815, 15.824889246588961, 16.470992125151032, 17.497576691578338, 16.568797685546439, 15.845972816102657, 17.375406965836859, 17.180285283986901, 15.948545208327705, 18.378749562212338, 18.680194272886567, 15.273878984241998, 18.975848668213622, 15.780059243290628, 19.027243991311014, 15.008263990878115, 14.397133907387381, 19.079656995933455, 17.678192220540996, 18.768805356915962, 19.84478410485557, 19.875063368320181, 19.875063368320181, 19.875063368320181, 19.875063368320181, 19.875063368320181, 19.875063368320181, 19.875063368320181, 19.875063368320181, 19.875063368320181, 19.875063368320181, 19.875063368320181, 19.875063368320181, 19.875063368320181, 19.875063368320181, 19.875063368320181, 19.875063368320181, 19.875063368320181, 19.875063368320181, 19.875063368320181, 19.875063368320181, 19.875063368320181, 19.875063368320181, 19.875063368320181, 19.875063368320181, 19.875063368320181, 19.875063368320181, 19.875063368320181, 19.875063368320181, 19.875063368320181, 19.875063368320181, 19.875063368320181, 19.875063368320181, 19.875063368320181, 19.875063368320181, 19.875063368320181, 19.875063368320181, 19.875063368320181, 19.875063368320181, 19.875063368320181, 19.875063368320181, 19.875063368320181, 19.875063368320181, 19.875063368320181, 19.875063368320181, 19.875063368320181, 19.875063368320181, 19.875063368320181]
f3=[11.630280444930502, 11.917332036717452, 12.087486525710416, 12.188313184238227, 12.267669225835583, 12.763440179383824, 13.031336447371698, 12.911472144651544, 13.411585161769908, 13.300063630710488, 13.456406226863681, 13.988467916898006, 13.84341614399078, 13.623906286203439, 13.846344813494701, 14.258954526791449, 13.984618086380477, 14.614975552894535, 14.191505143149067, 14.468075220973761, 14.599995045142142, 14.47398610334386, 14.286710943618035, 14.055798940401445, 14.822930030768177, 15.773229337482896, 14.959309787784008, 14.749649276523609, 16.315582393887535, 13.782878645959503, 14.950763825935628, 15.336104289858952, 16.09351462157332, 16.181127448765377, 16.527483675394222, 15.708698833834331, 16.232432692643005, 14.993723351450448, 14.855668765035995, 15.808954845268259, 15.450051566962157, 14.860933863377126, 15.575743764292604, 14.706160382438748, 14.580198609689488, 16.961584159097907, 16.57878230001192, 15.462057920651681, 15.647060603953623, 16.128988912621239, 15.637481204089951, 16.870731485125184, 16.624644576608773, 15.966990686413167, 17.410867844198364, 15.467427108208755, 16.475202428580296, 17.499815895889775, 17.197115736250403, 16.662692768224304, 17.261264829918098, 15.854353199187905, 16.454130400104251, 16.30182370239644, 18.704590092472102, 16.067537472358779, 16.831648021485488, 16.137111731305456, 16.969971479909081, 17.960087867478634, 16.921908207480808, 17.841456432424874, 17.895186165781045, 18.003363791965565, 20.384257367747949, 19.982521510235738, 19.890695765550593, 18.82584294075189, 20.376070802456717, 20.740294863206497, 20.837520164617789, 19.958202083745956, 19.949981435347581, 19.589613606384408, 20.680251723979417, 20.345614067467782, 20.50515154611475, 19.839575132406541, 20.201531508756208, 19.294739481779846, 20.716159982290872, 19.72597862751638, 19.808814018242273, 20.464185853648608, 19.260468549522091, 19.296953463515969, 19.871242211372202, 19.417928399534595, 19.962090664042886, 19.938292199552681, 20.253632955260812, 19.435438923661511, 19.815167698795008, 19.42218140435056, 20.392941082621888, 19.180202190848927, 20.642328630990846, 20.048457575951467, 20.500847589284284, 19.998697966127239, 18.569330217800402, 19.70099558432193, 19.46591291859437, 19.643540259677554, 19.416622295806039, 20.138483905518072, 19.519552605549897, 19.79342826244407, 19.637192516726827, 19.823291093750875, 20.318929504768988, 19.995813138255844, 19.785314223931881, 19.247358561957242, 19.545360389072904, 19.866848964589792, 19.552702714389916, 19.253981600565691, 19.979789666422469, 19.126410885006432, 20.3685584145632, 19.748421033738403, 20.381431059252066, 20.436899256672692, 19.82963339193136, 20.150277390319015, 20.215487426276081, 19.255326589413841, 20.185034732223457, 20.511211871354497, 19.200716135642498, 19.382553941388146, 18.848137418460489, 19.488475941094105, 20.378268960506702, 20.00556803006965, 20.211294396567283, 20.332050261157189, 20.449197858367473, 19.519378828605234, 19.296037757401521, 20.363240035076284, 18.935372529302789, 20.486918080060128, 18.870967686908688, 20.054399291191629, 20.820209097034954, 19.486896175499982, 18.963518504898545, 20.520027126888095, 18.981975748386699, 20.038568554141481, 19.444168354261301, 19.962002226667199, 19.676663980057615, 20.224012768119454, 19.911789555754343, 19.909612239917148, 19.345882828955219, 20.354302787075785, 20.390886649970867, 20.234381549653602, 20.363488770646129, 18.871940762455491, 20.05877659146487, 19.99238340274448, 20.075538055976772, 20.004324480753137, 20.145767043623334, 19.983561828804707, 19.805394864730825, 19.804952377767872, 19.813702227529969, 20.548911432264042, 19.237159500324914, 19.814307066498717, 20.28204182455908, 20.378275932453729, 21.179301987808081, 19.375368014508062, 20.049561343956984, 18.741943090429046, 19.619931583000088, 18.56129694500952, 19.81086659796269, 18.712472291278374, 22.025998726919187, 21.020516736955045, 18.347944412066326, 20.707425485281622, 17.991048225690843, 19.922943417916954, 18.939134394381259, 19.601875169550336, 19.763963584364408, 18.65233094685982, 20.516852271707865, 18.587926864101966, 19.73390604481737, 19.291461317370437, 18.732120301415097, 20.124567214077178, 20.448489775174725, 18.71349184542996, 20.532055190387567, 21.197110540908213, 18.822708363006981, 18.949793034327659, 20.063319757136004, 18.98608423805274, 20.887780704753691, 18.933417921663459, 19.606093342214471, 19.713891528019449, 19.02447406200675, 19.01366465056136, 20.415031661958452, 19.515130253256359, 18.757251341743142, 19.443087995147913, 17.844692594687746, 19.633271132504881, 18.027284281433765, 18.923037841505998, 18.502203797080266, 19.943229893709095, 19.845563334198321, 19.313083962785164, 17.87479566871713, 19.340169487652723, 20.36415281132706, 19.663318901475133, 18.697361279126291, 19.483605188745123, 19.04961156863191, 19.723341580567009, 18.842232669308402, 17.098654918026028, 18.031890609590608, 20.373135706845673, 19.598470342299105, 19.984959625978515, 17.309557373141324, 20.337461834775262, 20.125058093328672, 20.034068835430251, 20.162938756376825, 20.57947010416612, 20.104359554647793, 20.978632924566977, 20.287684332200698, 20.213382214654981, 20.874581867454445, 20.867851684629873, 20.764061930428639, 20.399697714841299, 20.588498890024454, 20.863219186820178, 20.484399272089419, 20.081664456193309, 20.918404717756964, 20.977681567880133, 20.983483265252705, 20.57061398248149, 21.046060407589859, 20.812025531513015, 20.821249300952321, 20.366159142456723, 21.077128921363901, 20.241017240720765, 20.727763944702687, 20.81657803563963, 20.830405322004072, 20.346430570465746, 20.155553273053837, 20.577158333435346, 20.372985298798731, 20.230928056836856, 20.575735648445377, 20.900231037950967, 20.97692992962568, 20.832133732799615, 20.859989132597399, 20.385429792800831, 20.854454870933814, 20.118285475995425, 21.039359670826492, 20.730842713698216, 21.107132505494612, 19.901700256402517]
#f4=[11.664719061747379, 11.828193287628538, 12.092795262272887, 12.406756404615402, 12.54441491234706, 12.673686943980046, 12.843874688106473, 13.302537569896424, 12.969524293632212, 13.331873905958293, 13.445936268234741, 13.559564967976126, 13.640243846180562, 13.525210684248828, 14.02882760827104, 13.654428735724798, 13.830919467118617, 14.350511111348567, 14.064711773305632, 14.810521580151814, 14.637029275404521, 14.394000628859711, 14.593225051817333, 15.056206773486984, 14.162878155603625, 15.442782310626633, 14.387912241323967, 14.814571186886628, 15.564814227585483, 14.425258870570209, 15.213709555894255, 14.950116794321731, 15.458531887217379, 15.050436019199093, 15.169126617046212, 15.393750475497825, 15.133568283223594, 16.203150716520884, 16.14271429685693, 15.722732526923471, 15.526912861759635, 16.451057138468734, 15.554912040494704, 16.203010243479284, 15.438458526436824, 16.530239736859709, 16.342969629702115, 16.986774085445578, 15.638348754536374, 15.188768147771137, 17.376094847867826, 14.785002737331306, 15.014193115815061, 16.589198702588533, 13.833377518898052, 14.069707350334097, 16.508304867308869, 16.537608133146293, 14.871958181595339, 17.128950155692738, 16.356572794780352, 17.393753475477531, 16.519046654026763, 16.978720664097729, 16.941678709624298, 15.383655489043329, 15.967987018076796, 16.954812312742543, 15.118301802439269, 14.005450796843373, 16.414927216313394, 17.755851610016677, 14.998014494614923, 16.940185626667425, 16.639382193761303, 15.933065629068167, 16.465427491687095, 14.033215327563168, 16.079558710267484, 16.141312007248921, 15.430714282254423, 16.572353035134668, 16.101773529168018, 14.410152560755229, 15.479322569606451, 17.637781811848491, 15.698646599722514, 15.320415674762096, 15.662683461918361, 16.029748881103771, 16.592991155426176, 15.12177510153211, 16.559461407364225, 15.168897380032375, 14.357393471877254, 14.709243713103625, 17.543266010750713, 13.904986515866266, 14.063258654813502, 16.16388682894409, 16.302206670517361, 15.44151308510218, 15.498069739402469, 16.325987661578459, 15.316871337505356, 14.794969734710991, 14.396087290337629, 15.361214952389137, 16.491405543576231, 16.742649744654305, 13.973869156158106, 15.495270293151371, 15.222704987939553, 16.212091900065175, 16.033793085695475, 14.62200052679616, 14.941530825252931, 16.648280083942261, 15.265688903853498, 15.335511749616362, 15.666190090460583, 15.436262759665807, 16.230460734956427, 16.388591744188609, 16.478249347214508, 14.256400473360424, 14.592537133970762, 15.747393822555694, 16.684050232788241, 16.183463755505116, 15.353533457391189, 16.56691079953378, 17.336220827765814, 15.811860284094152, 14.947803927251641, 15.761401107778989, 15.38697268193623, 16.936106169102217, 15.271038797203397, 14.69779281360773, 14.649944922834184, 18.192273211226787, 18.046691186576833, 14.861433634248959, 13.527853764962272, 14.482617366448954, 16.116288261417928, 18.582870623115205, 14.625787288463112, 16.473157412065419, 16.845233358872637, 14.992576719820143, 15.506852025915119, 17.544805096127131, 15.689145537294971, 16.29219679225746, 11.583040967565426, 16.037573512339705, 17.136132389664514, 14.339801573562161, 16.23966030965715, 14.052250424786706, 12.59903320692956, 16.313522586445188, 16.705192435419228, 14.885895083923105, 12.259719644483974, 13.079927100214935, 16.221594377854775, 15.698420845171942, 14.514555584923095, 17.06647926987219, 17.137572500036612, 17.643928366000534, 14.651451025811555, 16.302904697480081, 17.055926420358897, 16.006757286552062, 16.526943563079453, 17.449585525571855, 16.959805429860783, 16.849004148457762, 17.291588996586963, 16.397572521627133, 16.398778564211, 17.934003783701495, 16.831201596351701, 15.683450984073854, 16.229421963563816, 15.186760691538206, 16.719437477000653, 17.243966112907863, 16.622769109974644, 15.514475556226655, 17.604023080513105, 16.686173774792405, 16.301613729058648, 18.001339002308725, 17.347682975963121, 18.010100838130807, 16.196216028529882, 16.827441578554762, 17.788610888567007, 18.572063062980348, 15.605113870071328, 17.538315063546914, 17.682769925368028, 17.789903876216254, 15.841450672588024, 16.121924031466367, 15.597631195269917, 15.806702157130632, 14.746591012522932, 15.960971104623164, 15.953416119718417, 17.953074904104575, 16.100551693235037, 17.279703830827557, 15.954084833546448, 16.255841642269829, 18.533633305163839, 17.431927036468686, 17.627977554237219, 19.951909684497732, 13.596594772747196, 17.463522082446936, 14.710693944366838, 13.69764278539243, 16.990583287773525, 15.798882992312789, 15.517230824244077, 13.9767319952112, 16.36338037161584, 16.062935896352659, 15.335876589951688, 16.250799379216904, 15.062090431512136, 16.903332782667025, 16.21240761203358, 16.933460598100972, 14.895435307390137, 17.254224074339557, 16.125295177860224, 17.628805446391148, 15.037767888300802, 15.142164971519939, 15.385091336412598, 15.753353565876967, 16.622833046152195, 16.473318921558615, 14.675160550884044, 15.427704824703845, 16.818104035633741, 15.419117569888027, 16.312932760464307, 15.611061903218225, 15.714882810728435, 16.053375956932058, 14.16015211437448, 16.581336828633006, 14.747013496411663, 17.495415608710108, 17.100592622633496, 16.121902691080511, 15.345895071728838, 17.134097281324454, 15.822483926716062, 16.752428480218441, 15.985769906310317, 14.736421882476495, 16.184074122206802, 16.746353735807624, 16.76257435429271, 16.801468007798231, 17.36988852394699, 17.093057571884856, 16.097371623171483, 16.731636012297475, 17.031862227937946, 17.665844669322631, 16.728518367573557, 18.097957236571425, 16.288006036854746, 18.586643929111133, 15.44031986707342, 17.544527839074814, 16.661385135704634, 14.860765480835541, 16.287135034795831, 16.713691838701209, 17.500714057884355, 15.031619680335014, 14.670245761842299, 17.021138998790626, 18.777892979754423, 18.401631410076043, 15.945128702504249, 14.906797211307296, 17.346189322163433, 14.814039272770771]
f4=[11.577435, 11.76477, 12.040824, 12.245099, 12.346799, 12.493817, 12.465278, 12.819153, 12.923781, 12.995482, 12.946593, 13.396244, 13.86723, 13.72754, 14.298023, 13.860069, 13.447259, 14.334724, 13.818694, 13.89067, 13.979795, 14.440431, 14.348933, 15.05792, 15.081063, 15.359482, 15.369892, 15.145353, 15.445351, 16.209336, 16.211397, 15.56029, 15.877928, 16.016664, 15.717962, 15.993634, 15.728489, 15.239821, 15.856827, 16.131129, 16.188919, 15.867658, 14.978999, 16.163646, 16.960477, 15.06629, 16.091564, 16.818483, 17.47548, 15.395629, 16.699844, 15.920453, 15.547141, 17.448814, 16.592512, 16.251969, 16.470042, 16.301587, 18.529858, 16.448662, 17.646247, 18.061483, 17.567119, 17.052815, 13.910295, 17.737704, 16.773676, 16.872298, 18.127677, 17.02115, 17.546273, 18.134541, 15.890795, 16.205818, 18.024137, 18.408018, 17.523193, 17.301651, 15.824159, 15.407307, 15.249798, 16.544648, 15.321728, 15.297184, 15.764968, 16.842277, 14.182086, 16.930323, 16.477502, 17.392045, 18.49368, 16.941481, 16.67565, 16.232228, 15.050067, 16.420805, 16.431007, 15.726302, 15.926244, 17.058496, 17.583521, 16.307854, 16.527519, 16.982501, 16.03996, 16.520764, 17.047658, 16.276838, 18.006622, 14.456373, 13.000632, 16.078707, 15.747553, 16.00205, 16.950017, 16.791592, 16.480829, 15.780724, 16.545234, 17.071292, 15.263358, 16.526963, 15.678332, 15.238112, 17.434038, 16.525104, 17.515015, 18.222845, 15.175422, 17.043363, 15.451051, 15.286651, 16.400998, 13.946862, 16.69807, 15.191941, 14.979431, 15.993578, 16.178035, 15.81919, 16.627415, 15.015619, 15.887237, 16.439681, 16.744834, 15.109171, 14.539325, 15.704611, 14.790918, 15.327382, 13.950446, 15.66125, 15.922053, 14.566649, 16.006563, 14.521033, 14.9254, 16.032611, 17.124401, 14.618361, 15.489776, 15.659393, 13.537703, 15.898022, 15.953369, 15.53934, 15.582785, 15.423574, 14.875788, 15.372497, 16.535845, 15.380345, 15.908046, 16.734119, 13.983036, 15.611445, 15.726681, 15.806976, 15.95054, 14.487382, 16.218616, 15.753317, 16.01589, 17.062927, 16.381083, 16.397765, 13.835836, 14.986351, 13.932337, 15.379899, 15.789567, 15.134758, 17.505989, 16.092074, 16.771725, 16.317821, 16.071367, 15.989365, 14.939045, 15.282329, 14.464641, 15.767366, 15.790258, 14.921053, 15.21098, 14.296069, 15.408024, 15.565171, 15.141683, 16.157657, 16.842292, 16.454449, 14.700801, 16.196978, 14.21397, 15.395853, 14.360085, 16.005448, 14.529424, 14.642746, 16.448252, 15.362774, 16.863837, 15.125013, 14.061601, 15.096118, 15.655458, 14.357157, 14.966165, 13.756601, 16.499616, 15.772774, 14.844139, 15.092738, 15.010894, 16.293122, 14.317233, 15.35853, 16.064056, 15.702805, 15.851317, 15.99261, 16.350325, 14.61444, 16.625866, 16.745729, 15.915595, 16.743685, 14.158828, 14.610198, 14.465641, 15.759085, 15.337512, 16.092652, 16.860649, 12.926327, 16.315451, 15.734146, 16.113677, 16.51387, 16.752013, 15.529992, 15.948644, 15.431291, 16.355448, 16.723073, 15.879335, 16.384115, 15.331101, 15.856215, 15.16604, 15.897101, 16.534428, 15.095361, 14.81648, 16.295051, 16.16309, 17.313501, 16.084941, 16.004345, 16.178608, 17.574014, 16.136898, 15.929211, 15.912996, 15.945909, 17.046406, 16.838939, 16.522814, 14.416148, 16.203795, 16.026793, 16.182718, 15.826033, 15.709262, 16.671581, 15.899134, 17.785233, 16.589489, 14.785156]
plt.plot(x, f1, marker='None', color='chartreuse', label=u'm=100')
plt.plot(x, f2, marker='None', color='deeppink', label=u'm=200')
plt.plot(x, f3, marker='None', color='deepskyblue', label=u'm=500')
plt.plot(x, f4, marker='None', color='darkorchid', label=u'm=1000')
plt.ylim(ymin = 10)
plt.ylim(ymax = 25)
plt.xlim(xmin = 0)
plt.xlim(xmax = 300)
plt.xlabel(u'迭代次数',fontproperties='SimHei')
plt.ylabel(u'类别可分性判据',fontproperties='SimHei')
plt.title(u'不同种群数量对于结果的影响',fontproperties='SimHei')
plt.legend()
plt.show()

