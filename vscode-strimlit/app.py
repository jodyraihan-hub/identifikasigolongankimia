import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
import random

# Konfigurasi halaman
st.set_page_config(
    page_title="Analisis Kation Golongan I-V",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Custom untuk styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #ff7f0e;
        margin-bottom: 1rem;
    }
    .reaction-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .cation-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border: 2px solid #e0e0e0;
    }
    .quiz-option {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s;
    }
    .quiz-option:hover {
        background-color: #e3f2fd;
        transform: translateX(5px);
    }
    .correct {
        background-color: #c8e6c9 !important;
        border: 2px solid #4caf50;
    }
    .wrong {
        background-color: #ffcdd2 !important;
        border: 2px solid #f44336;
    }
    .step-number {
        background-color: #1f77b4;
        color: white;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        margin-right: 10px;
    }
    .precipitate-white { color: #9e9e9e; font-weight: bold; }
    .precipitate-yellow { color: #ffc107; font-weight: bold; }
    .precipitate-black { color: #212121; font-weight: bold; }
    .solution-blue { color: #2196f3; font-weight: bold; }
    .solution-red { color: #f44336; font-weight: bold; }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #fff;
        border-radius: 4px 4px 0 0;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1f77b4;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Data kation berdasarkan bagan
cation_data = {
    "Golongan I (Ag⁺, Pb²⁺, Hg₂²⁺)": {
        "color": "#FF6B6B",
        "reagen": "HCl encer",
        "precipitate": "AgCl (putih), PbCl₂ (putih), Hg₂Cl₂ (putih)",
        "steps": [
            {
                "action": "Tambahkan H₂O panas",
                "result": "PbCl₂ larut, AgCl dan Hg₂Cl₂ tidak larut",
                "filtrate": "Pb²⁺",
                "residue": "AgCl, Hg₂Cl₂"
            },
            {
                "action": "Pada filtrat Pb²⁺: Tambahkan K₂CrO₄",
                "result": "Endapan kuning PbCrO₄",
                "confirm": "Pb²⁺ terkonfirmasi"
            },
            {
                "action": "Pada residu AgCl, Hg₂Cl₂: Tambahkan NH₄OH",
                "result": "AgCl larut membentuk [Ag(NH₃)₂]⁺, Hg₂Cl₂ berubah menjadi Hg (hitam) + Hg(NH₂)Cl (putih)",
                "filtrate": "[Ag(NH₃)₂]⁺",
                "residue": "Hg (hitam) + Hg(NH₂)Cl (putih)"
            },
            {
                "action": "Pada filtrat [Ag(NH₃)₂]⁺: Tambahkan HNO₃",
                "result": "Endapan putih AgCl kembali terbentuk",
                "confirm": "Ag⁺ terkonfirmasi"
            }
        ]
    },
    "Golongan II (Al³⁺, Fe³⁺, Ba²⁺, Sr²⁺, Ca²⁺)": {
        "color": "#4ECDC4",
        "reagen": "NH₄OH berlebih + NH₄Cl",
        "precipitate": "Al(OH)₃ (putih/gel), Fe(OH)₃ (coklat/merah), Ba²⁺, Sr²⁺, Ca²⁺ tetap dalam larutan",
        "steps": [
            {
                "action": "Endapan: Tambahkan NaOH berlebih",
                "result": "Al(OH)₃ larut membentuk [Al(OH)₄]⁻, Fe(OH)₃ tidak larut",
                "filtrate": "[Al(OH)₄]⁻",
                "residue": "Fe(OH)₃"
            },
            {
                "action": "Pada filtrat [Al(OH)₄]⁻: Tambahkan HCl (asam) perlahan",
                "result": "Endapan putih/gel Al(OH)₃ kembali",
                "confirm": "Al³⁺ terkonfirmasi"
            },
            {
                "action": "Pada residu Fe(OH)₃: Tambahkan HNO₃ + KSCN",
                "result": "Larutan merah darah [Fe(SCN)]²⁺",
                "confirm": "Fe³⁺ terkonfirmasi"
            },
            {
                "action": "Pada filtrat awal (Ba²⁺, Sr²⁺, Ca²⁺): Tambahkan K₂CrO₄",
                "result": "Endapan kuning BaCrO₄, Sr²⁺ dan Ca²⁺ tetap larut",
                "filtrate": "Sr²⁺, Ca²⁺",
                "residue": "BaCrO₄ (kuning)"
            },
            {
                "action": "Pada filtrat Sr²⁺, Ca²⁺: Tambahkan (NH₄)₂C₂O₄",
                "result": "Endapan putih CaC₂O₄, Sr²⁺ tetap larut",
                "filtrate": "Sr²⁺",
                "residue": "CaC₂O₄ (putih)"
            },
            {
                "action": "Pada filtrat Sr²⁺: Tambahkan Na₂CO₃ panas",
                "result": "Endapan putih SrCO₃",
                "confirm": "Sr²⁺ terkonfirmasi"
            }
        ]
    }
}

# Data kuis berdasarkan bagan
quiz_data = [
    {
        "question": "Kation manakah yang membentuk endapan putih dengan HCl encer, kemudian larut dalam air panas?",
        "options": ["Ag⁺", "Pb²⁺", "Hg₂²⁺", "Ba²⁺"],
        "correct": 1,
        "explanation": "PbCl₂ membentuk endapan putih dengan HCl encer dan larut dalam air panas, sedangkan AgCl dan Hg₂Cl₂ tidak larut."
    },
    {
        "question": "Apa warna endapan yang terbentuk saat Pb²⁺ direaksikan dengan K₂CrO₄?",
        "options": ["Putih", "Kuning", "Hitam", "Merah"],
        "correct": 1,
        "explanation": "PbCrO₄ membentuk endapan berwarna kuning."
    },
    {
        "question": "Bagaimana perbedaan antara AgCl dan Hg₂Cl₂ saat ditambahkan NH₄OH?",
        "options": [
            "Keduanya larut",
            "AgCl larut, Hg₂Cl₂ berubah menjadi hitam + putih",
            "Keduanya tidak larut",
            "Hg₂Cl₂ larut, AgCl tidak larut"
        ],
        "correct": 1,
        "explanation": "AgCl larut dalam NH₄OH membentuk kompleks [Ag(NH₃)₂]⁺, sedangkan Hg₂Cl₂ mengalami disproporsionasi menjadi Hg (hitam) dan Hg(NH₂)Cl (putih)."
    },
    {
        "question": "Kation manakah yang membentuk endapan coklat/merah dengan NH₄OH?",
        "options": ["Al³⁺", "Fe³⁺", "Ba²⁺", "Ca²⁺"],
        "correct": 1,
        "explanation": "Fe(OH)₃ membentuk endapan berwarna coklat/merah, sedangkan Al(OH)₃ berwarna putih."
    },
    {
        "question": "Apa yang terjadi pada Al(OH)₃ saat ditambahkan NaOH berlebih?",
        "options": [
            "Tetap sebagai endapan",
            "Larut membentuk [Al(OH)₄]⁻",
            "Berubah warna menjadi merah",
            "Mengendap lebih banyak"
        ],
        "correct": 1,
        "explanation": "Al(OH)₃ bersifat amfoter dan larut dalam NaOH berlebih membentuk ion aluminate [Al(OH)₄]⁻."
    },
    {
        "question": "Reagen apa yang digunakan untuk mengkonfirmasi Fe³⁺?",
        "options": ["K₂CrO₄", "KSCN", "NH₄OH", "HCl"],
        "correct": 1,
        "explanation": "Fe³⁺ membentuk kompleks merah darah [Fe(SCN)]²⁺ dengan KSCN."
    },
    {
        "question": "Kation manakah yang membentuk endapan kuning dengan K₂CrO₄ dalam golongan II?",
        "options": ["Sr²⁺", "Ca²⁺", "Ba²⁺", "Al³⁺"],
        "correct": 2,
        "explanation": "BaCrO₄ membentuk endapan kuning, sedangkan Sr²⁺ dan Ca²⁺ tidak bereaksi dengan K₂CrO₄ dalam kondisi ini."
    },
    {
        "question": "Apa warna endapan CaC₂O₄ yang terbentuk dari reaksi Ca²⁺ dengan (NH₄)₂C₂O₄?",
        "options": ["Kuning", "Putih", "Hitam", "Merah"],
        "correct": 1,
        "explanation": "CaC₂O₄ (kalsium oksalat) membentuk endapan putih."
    },
    {
        "question": "Mengapa NH₄Cl ditambahkan bersama NH₄OH dalam pengendapan golongan II?",
        "options": [
            "Sebagai katalis",
            "Menekan ionisasi NH₄OH sehingga OH⁻ cukup untuk Mg(OH)₂ saja",
            "Memberikan warna",
            "Menghasilkan panas"
        ],
        "correct": 1,
        "explanation": "NH₄Cl menekan ionisasi NH₄OH (efek ion senama) sehingga konsentrasi OH⁻ cukup untuk mengendapkan Al(OH)₃ dan Fe(OH)₃ tetapi tidak cukup untuk Mg(OH)₂."
    },
    {
        "question": "Kation manakah yang terakhir dikonfirmasi dalam analisis golongan II menggunakan Na₂CO₃ panas?",
        "options": ["Ba²⁺", "Ca²⁺", "Sr²⁺", "Fe³⁺"],
        "correct": 2,
        "explanation": "Sr²⁺ dikonfirmasi terakhir dengan membentuk endapan putih SrCO₃ menggunakan Na₂CO₃ panas."
    }
]

# Sidebar navigation
st.sidebar.title("🧪 Navigasi")
page = st.sidebar.radio(
    "Pilih Menu:",
    ["🏠 Beranda", "📊 Bagan Interaktif", "🔬 Detail Reaksi", "📝 Kuis", "📚 Referensi"]
)

# Fungsi untuk membuat node graph
def create_flowchart_nodes():
    nodes = []
    edges = []

    # Level 0 - Sample
    nodes.append(Node(id="sample", label="Sampel\n(Ag⁺, Pb²⁺, Hg₂²⁺,\nAl³⁺, Fe³⁺, Ba²⁺,\nSr²⁺, Ca²⁺)", 
                     color="#9C27B0", size=30, shape="box"))

    # Level 1 - Group I
    nodes.append(Node(id="hcl", label="+ HCl encer", color="#FF9800", size=25))
    nodes.append(Node(id="group1", label="Endapan Putih\n(AgCl, PbCl₂, Hg₂Cl₂)", 
                     color="#FF6B6B", size=28, shape="box"))
    nodes.append(Node(id="group2", label="Filtrat\n(Al³⁺, Fe³⁺, Ba²⁺,\nSr²⁺, Ca²⁺)", 
                     color="#4ECDC4", size=28, shape="box"))

    edges.append(Edge(source="sample", target="hcl", color="#666"))
    edges.append(Edge(source="hcl", target="group1", color="#666"))
    edges.append(Edge(source="hcl", target="group2", color="#666"))

    # Group I branches
    nodes.append(Node(id="hot_water", label="+ H₂O panas", color="#FF9800", size=25))
    nodes.append(Node(id="pb", label="Pb²⁺\n(larut)", color="#FFD93D", size=25, shape="box"))
    nodes.append(Node(id="ag_hg", label="AgCl, Hg₂Cl₂\n(tidak larut)", 
                     color="#FF6B6B", size=25, shape="box"))

    edges.append(Edge(source="group1", target="hot_water", color="#666"))
    edges.append(Edge(source="hot_water", target="pb", color="#666"))
    edges.append(Edge(source="hot_water", target="ag_hg", color="#666"))

    # Pb confirmation
    nodes.append(Node(id="k2cro4", label="+ K₂CrO₄", color="#FF9800", size=25))
    nodes.append(Node(id="pbcro4", label="PbCrO₄\n(Kuning)", color="#FFD93D", size=25, shape="box"))
    edges.append(Edge(source="pb", target="k2cro4", color="#666"))
    edges.append(Edge(source="k2cro4", target="pbcro4", color="#666"))

    # Ag/Hg branch
    nodes.append(Node(id="nh4oh", label="+ NH₄OH", color="#FF9800", size=25))
    nodes.append(Node(id="ag_complex", label="[Ag(NH₃)₂]⁺\n(larut)", color="#C8E6C9", size=25, shape="box"))
    nodes.append(Node(id="hg_mix", label="Hg + Hg(NH₂)Cl\n(Hitam + Putih)", 
                     color="#757575", size=25, shape="box"))

    edges.append(Edge(source="ag_hg", target="nh4oh", color="#666"))
    edges.append(Edge(source="nh4oh", target="ag_complex", color="#666"))
    edges.append(Edge(source="nh4oh", target="hg_mix", color="#666"))

    # Ag confirmation
    nodes.append(Node(id="hno3", label="+ HNO₃", color="#FF9800", size=25))
    nodes.append(Node(id="agcl_back", label="AgCl\n(Putih)", color="#E0E0E0", size=25, shape="box"))
    edges.append(Edge(source="ag_complex", target="hno3", color="#666"))
    edges.append(Edge(source="hno3", target="agcl_back", color="#666"))

    # Group II branches
    nodes.append(Node(id="nh4oh_group2", label="+ NH₄OH + NH₄Cl", color="#FF9800", size=25))
    nodes.append(Node(id="precipitate2", label="Endapan\nAl(OH)₃ (Putih/Gel)\nFe(OH)₃ (Coklat)", 
                     color="#FF6B6B", size=28, shape="box"))
    nodes.append(Node(id="filtrate2", label="Filtrat\nBa²⁺, Sr²⁺, Ca²⁺", 
                     color="#4ECDC4", size=28, shape="box"))

    edges.append(Edge(source="group2", target="nh4oh_group2", color="#666"))
    edges.append(Edge(source="nh4oh_group2", target="precipitate2", color="#666"))
    edges.append(Edge(source="nh4oh_group2", target="filtrate2", color="#666"))

    # Al/Fe separation
    nodes.append(Node(id="naoh", label="+ NaOH berlebih", color="#FF9800", size=25))
    nodes.append(Node(id="al_complex", label="[Al(OH)₄]⁻\n(larut)", color="#C8E6C9", size=25, shape="box"))
    nodes.append(Node(id="fe_oh", label="Fe(OH)₃\n(tidak larut)", color="#8D6E63", size=25, shape="box"))

    edges.append(Edge(source="precipitate2", target="naoh", color="#666"))
    edges.append(Edge(source="naoh", target="al_complex", color="#666"))
    edges.append(Edge(source="naoh", target="fe_oh", color="#666"))

    # Al confirmation
    nodes.append(Node(id="hcl_slow", label="+ HCl perlahan", color="#FF9800", size=25))
    nodes.append(Node(id="al_oh_back", label="Al(OH)₃\n(Putih/Gel)", color="#E0E0E0", size=25, shape="box"))
    edges.append(Edge(source="al_complex", target="hcl_slow", color="#666"))
    edges.append(Edge(source="hcl_slow", target="al_oh_back", color="#666"))

    # Fe confirmation
    nodes.append(Node(id="kscn", label="+ KSCN", color="#FF9800", size=25))
    nodes.append(Node(id="fe_red", label="[Fe(SCN)]²⁺\n(Merah Darah)", color="#F44336", size=25, shape="box"))
    edges.append(Edge(source="fe_oh", target="kscn", color="#666"))
    edges.append(Edge(source="kscn", target="fe_red", color="#666"))

    # Ba/Sr/Ca separation
    nodes.append(Node(id="k2cro4_2", label="+ K₂CrO₄", color="#FF9800", size=25))
    nodes.append(Node(id="ba_cro4", label="BaCrO₄\n(Kuning)", color="#FFD93D", size=25, shape="box"))
    nodes.append(Node(id="sr_ca", label="Sr²⁺, Ca²⁺\n(larut)", color="#4ECDC4", size=25, shape="box"))

    edges.append(Edge(source="filtrate2", target="k2cro4_2", color="#666"))
    edges.append(Edge(source="k2cro4_2", target="ba_cro4", color="#666"))
    edges.append(Edge(source="k2cro4_2", target="sr_ca", color="#666"))

    # Sr/Ca separation
    nodes.append(Node(id="oxalate", label="+ (NH₄)₂C₂O₄", color="#FF9800", size=25))
    nodes.append(Node(id="ca_ox", label="CaC₂O₄\n(Putih)", color="#E0E0E0", size=25, shape="box"))
    nodes.append(Node(id="sr_only", label="Sr²⁺\n(larut)", color="#4ECDC4", size=25, shape="box"))

    edges.append(Edge(source="sr_ca", target="oxalate", color="#666"))
    edges.append(Edge(source="oxalate", target="ca_ox", color="#666"))
    edges.append(Edge(source="oxalate", target="sr_only", color="#666"))

    # Sr confirmation
    nodes.append(Node(id="na2co3", label="+ Na₂CO₃ panas", color="#FF9800", size=25))
    nodes.append(Node(id="srco3", label="SrCO₃\n(Putih)", color="#E0E0E0", size=25, shape="box"))
    edges.append(Edge(source="sr_only", target="na2co3", color="#666"))
    edges.append(Edge(source="na2co3", target="srco3", color="#666"))

    return nodes, edges

# Halaman Beranda
if page == "🏠 Beranda":
    st.markdown('<h1 class="main-header">🧪 Analisis Kation Golongan I-V</h1>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        <div style="font-size: 1.2rem; line-height: 1.8;">
        <p>Selamat datang di aplikasi <strong>Analisis Kation Golongan I-V</strong>!</p>
        <p>Aplikasi ini dirancang untuk membantu Anda memahami skema analisis kation secara sistematis berdasarkan bagan reaksi kimia.</p>

        <h3 style="color: #1f77b4;">📋 Fitur Utama:</h3>
        <ul>
            <li><strong>Bagan Interaktif</strong> - Visualisasi lengkap alur analisis kation</li>
            <li><strong>Detail Reaksi</strong> - Penjelasan step-by-step setiap reaksi</li>
            <li><strong>Kuis Interaktif</strong> - Uji pemahaman Anda dengan 10 soal pilihan ganda</li>
            <li><strong>Referensi</strong> - Tabel ringkasan reaksi dan warna endapan</li>
        </ul>

        <h3 style="color: #1f77b4;">🔬 Kation yang Dianalisis:</h3>
        <table style="width:100%; border-collapse: collapse;">
            <tr style="background-color: #f0f2f6;">
                <th style="padding: 10px; border: 1px solid #ddd;">Golongan</th>
                <th style="padding: 10px; border: 1px solid #ddd;">Kation</th>
                <th style="padding: 10px; border: 1px solid #ddd;">Reagen Pengendap</th>
            </tr>
            <tr>
                <td style="padding: 10px; border: 1px solid #ddd;"><strong>Golongan I</strong></td>
                <td style="padding: 10px; border: 1px solid #ddd;">Ag⁺, Pb²⁺, Hg₂²⁺</td>
                <td style="padding: 10px; border: 1px solid #ddd;">HCl encer</td>
            </tr>
            <tr style="background-color: #f9f9f9;">
                <td style="padding: 10px; border: 1px solid #ddd;"><strong>Golongan II</strong></td>
                <td style="padding: 10px; border: 1px solid #ddd;">Al³⁺, Fe³⁺, Ba²⁺, Sr²⁺, Ca²⁺</td>
                <td style="padding: 10px; border: 1px solid #ddd;">NH₄OH + NH₄Cl</td>
            </tr>
        </table>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background-color: #e3f2fd; padding: 20px; border-radius: 15px; margin-top: 20px;">
            <h3 style="color: #1565c0;">💡 Tips Penggunaan</h3>
            <ol>
                <li>Pelajari <strong>Bagan Interaktif</strong> untuk memahami alur analisis</li>
                <li>Baca <strong>Detail Reaksi</strong> untuk memahami setiap langkah</li>
                <li>Uji pemahaman dengan <strong>Kuis</strong></li>
                <li>Gunakan <strong>Referensi</strong> untuk mengingat kembali</li>
            </ol>
            <p style="margin-top: 20px; font-style: italic; color: #555;">
                "Kimia analitik adalah seni memisahkan dan mengidentifikasi"
            </p>
        </div>
        """, unsafe_allow_html=True)

# Halaman Bagan Interaktif
elif page == "📊 Bagan Interaktif":
    st.markdown('<h1 class="main-header">📊 Bagan Analisis Kation</h1>', unsafe_allow_html=True)

    st.info("🖱️ **Cara menggunakan:** Klik dan drag untuk navigasi, scroll untuk zoom. Hover pada node untuk melihat detail.")

    nodes, edges = create_flowchart_nodes()

    config = Config(
        width=1200,
        height=800,
        directed=True,
        physics=True,
        hierarchical=True,
        nodeHighlightBehavior=True,
        highlightColor="#F57C00",
        collapsible=True,
        node={'labelProperty': 'label'},
        link={'labelProperty': 'label', 'renderLabel': False},
        hierarchicalLayout={
            'direction': 'UD',
            'sortMethod': 'directed',
            'levelSeparation': 150,
            'nodeSpacing': 200
        }
    )

    return_value = agraph(nodes=nodes, edges=edges, config=config)

    if return_value:
        st.success(f"Anda memilih: **{return_value}**")

        # Tampilkan detail berdasarkan node yang dipilih
        node_details = {
            "sample": "Sampel awal mengandung kation: Ag⁺, Pb²⁺, Hg₂²⁺, Al³⁺, Fe³⁺, Ba²⁺, Sr²⁺, Ca²⁺",
            "group1": "Endapan putih terbentuk: AgCl, PbCl₂, Hg₂Cl₂. Endapan ini tidak larut dalam air dingin.",
            "group2": "Filtrat mengandung kation golongan II yang tidak terendap oleh HCl encer.",
            "pb": "PbCl₂ larut dalam air panas karena kelarutannya meningkat dengan suhu.",
            "ag_hg": "AgCl dan Hg₂Cl₂ tidak larut dalam air panas.",
            "pbcro4": "PbCrO₄ adalah endapan kuning yang mengkonfirmasi keberadaan Pb²⁺.",
            "ag_complex": "[Ag(NH₃)₂]⁺ adalah kompleks diamminperak(I) yang larut.",
            "hg_mix": "Hg₂Cl₂ mengalami disproporsionasi: Hg₂²⁺ → Hg⁰ + Hg²⁺",
            "agcl_back": "AgCl terendap kembali saat ditambahkan asam kuat (HNO₃).",
            "precipitate2": "Al(OH)₃ (putih/gel) dan Fe(OH)₃ (coklat/merah) terendap.",
            "filtrate2": "Ba²⁺, Sr²⁺, Ca²⁺ tetap dalam larutan sebagai ion bebas.",
            "al_complex": "Al(OH)₃ bersifat amfoter dan larut dalam basa kuat berlebih.",
            "fe_oh": "Fe(OH)₃ tidak larut dalam basa berlebih (bersifat basa).",
            "al_oh_back": "Al(OH)₃ terendap kembali saat ditambahkan asam perlahan.",
            "fe_red": "[Fe(SCN)]²⁺ adalah kompleks berwarna merah darah yang sangat sensitif.",
            "ba_cro4": "BaCrO₄ berwarna kuning dan tidak larut dalam asam asetat.",
            "ca_ox": "CaC₂O₄ (kalsium oksalat) berwarna putih.",
            "srco3": "SrCO₃ berwarna putih dan terbentuk dalam kondisi panas."
        }

        if return_value in node_details:
            st.markdown(f'<div class="reaction-box">{node_details[return_value]}</div>', 
                       unsafe_allow_html=True)

# Halaman Detail Reaksi
elif page == "🔬 Detail Reaksi":
    st.markdown('<h1 class="main-header">🔬 Detail Reaksi Analisis</h1>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Golongan I (Ag⁺, Pb²⁺, Hg₂²⁺)", "Golongan II (Al³⁺, Fe³⁺, Ba²⁺, Sr²⁺, Ca²⁺)"])

    with tab1:
        st.markdown('<h2 class="sub-header">Analisis Golongan I</h2>', unsafe_allow_html=True)

        st.markdown("""
        <div class="cation-card">
            <h3>🧪 Reagen Pengendap: HCl encer</h3>
            <p><strong>Reaksi:</strong></p>
            <ul>
                <li>Ag⁺ + Cl⁻ → <span class="precipitate-white">AgCl↓ (Putih)</span></li>
                <li>Pb²⁺ + 2Cl⁻ → <span class="precipitate-white">PbCl₂↓ (Putih)</span></li>
                <li>Hg₂²⁺ + 2Cl⁻ → <span class="precipitate-white">Hg₂Cl₂↓ (Putih)</span></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        for i, step in enumerate(cation_data["Golongan I (Ag⁺, Pb²⁺, Hg₂²⁺)"]["steps"], 1):
            with st.expander(f"Langkah {i}: {step['action']}"):
                st.markdown(f"""
                <div class="reaction-box">
                    <p><strong>Aksi:</strong> {step['action']}</p>
                    <p><strong>Hasil:</strong> {step['result']}</p>
                    {f'<p><strong>Filtrat:</strong> {step["filtrate"]}</p>' if 'filtrate' in step else ''}
                    {f'<p><strong>Residu:</strong> {step["residue"]}</p>' if 'residue' in step else ''}
                    {f'<p><strong>Konfirmasi:</strong> <span style="color: green;">{step["confirm"]}</span></p>' if 'confirm' in step else ''}
                </div>
                """, unsafe_allow_html=True)

    with tab2:
        st.markdown('<h2 class="sub-header">Analisis Golongan II</h2>', unsafe_allow_html=True)

        st.markdown("""
        <div class="cation-card">
            <h3>🧪 Reagen Pengendap: NH₄OH + NH₄Cl</h3>
            <p><strong>Reaksi:</strong></p>
            <ul>
                <li>Al³⁺ + 3OH⁻ → <span class="precipitate-white">Al(OH)₃↓ (Putih/Gel)</span></li>
                <li>Fe³⁺ + 3OH⁻ → <span class="precipitate-white" style="color: #8D6E63;">Fe(OH)₃↓ (Coklat/Merah)</span></li>
                <li>Ba²⁺, Sr²⁺, Ca²⁺ tetap dalam larutan</li>
            </ul>
            <p><em>NH₄Cl berfungsi sebagai penyangga untuk menekan [OH⁻] agar Mg²⁺ tidak ikut terendap</em></p>
        </div>
        """, unsafe_allow_html=True)

        for i, step in enumerate(cation_data["Golongan II (Al³⁺, Fe³⁺, Ba²⁺, Sr²⁺, Ca²⁺)"]["steps"], 1):
            with st.expander(f"Langkah {i}: {step['action']}"):
                st.markdown(f"""
                <div class="reaction-box">
                    <p><strong>Aksi:</strong> {step['action']}</p>
                    <p><strong>Hasil:</strong> {step['result']}</p>
                    {f'<p><strong>Filtrat:</strong> {step["filtrate"]}</p>' if 'filtrate' in step else ''}
                    {f'<p><strong>Residu:</strong> {step["residue"]}</p>' if 'residue' in step else ''}
                    {f'<p><strong>Konfirmasi:</strong> <span style="color: green;">{step["confirm"]}</span></p>' if 'confirm' in step else ''}
                </div>
                """, unsafe_allow_html=True)

# Halaman Kuis
elif page == "📝 Kuis":
    st.markdown('<h1 class="main-header">📝 Kuis Analisis Kation</h1>', unsafe_allow_html=True)

    if 'quiz_state' not in st.session_state:
        st.session_state.quiz_state = {
            'current_question': 0,
            'score': 0,
            'answered': False,
            'selected_option': None,
            'show_result': False,
            'shuffled_questions': random.sample(quiz_data, len(quiz_data))
        }

    state = st.session_state.quiz_state

    # Progress bar
    progress = (state['current_question']) / len(quiz_data)
    st.progress(progress)
    st.write(f"Soal {state['current_question'] + 1} dari {len(quiz_data)}")

    if state['current_question'] < len(quiz_data):
        q = state['shuffled_questions'][state['current_question']]

        st.markdown(f"""
        <div class="cation-card">
            <h3>{q['question']}</h3>
        </div>
        """, unsafe_allow_html=True)

        # Tampilkan opsi
        for i, option in enumerate(q['options']):
            col1, col2 = st.columns([1, 10])
            with col1:
                st.write(f"{chr(65+i)}.")
            with col2:
                if not state['answered']:
                    if st.button(option, key=f"opt_{i}", use_container_width=True):
                        state['answered'] = True
                        state['selected_option'] = i
                        if i == q['correct']:
                            state['score'] += 1
                        st.rerun()
                else:
                    if i == q['correct']:
                        st.markdown(f'<div class="quiz-option correct">✅ {option}</div>', 
                                   unsafe_allow_html=True)
                    elif i == state['selected_option'] and i != q['correct']:
                        st.markdown(f'<div class="quiz-option wrong">❌ {option}</div>', 
                                   unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="quiz-option">{option}</div>', 
                                   unsafe_allow_html=True)

        if state['answered']:
            st.markdown(f"""
            <div class="reaction-box" style="margin-top: 20px;">
                <h4>💡 Penjelasan:</h4>
                <p>{q['explanation']}</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Soal Berikutnya →", type="primary", use_container_width=True):
                state['current_question'] += 1
                state['answered'] = False
                state['selected_option'] = None
                st.rerun()
    else:
        # Hasil akhir
        score_percent = (state['score'] / len(quiz_data)) * 100

        st.markdown(f"""
        <div class="cation-card" style="text-align: center;">
            <h1>🎉 Kuis Selesai!</h1>
            <h2>Skor Anda: {state['score']}/{len(quiz_data)} ({score_percent:.0f}%)</h2>
        </div>
        """, unsafe_allow_html=True)

        if score_percent >= 80:
            st.balloons()
            st.success("🏆 Luar biasa! Anda menguasai materi analisis kation dengan sangat baik!")
        elif score_percent >= 60:
            st.info("👍 Bagus! Pemahaman Anda sudah cukup baik, tingkatkan lagi!")
        else:
            st.warning("📚 Perlu belajar lagi. Pelajari bagan dan detail reaksi dengan lebih teliti.")

        if st.button("🔄 Ulangi Kuis", type="primary", use_container_width=True):
            st.session_state.quiz_state = {
                'current_question': 0,
                'score': 0,
                'answered': False,
                'selected_option': None,
                'show_result': False,
                'shuffled_questions': random.sample(quiz_data, len(quiz_data))
            }
            st.rerun()

# Halaman Referensi
elif page == "📚 Referensi":
    st.markdown('<h1 class="main-header">📚 Tabel Referensi</h1>', unsafe_allow_html=True)

    st.markdown("""
    <div class="cation-card">
        <h3>🎨 Warna Endapan dan Larutan</h3>
        <table style="width:100%; border-collapse: collapse;">
            <tr style="background-color: #1f77b4; color: white;">
                <th style="padding: 12px; border: 1px solid #ddd;">Senyawa</th>
                <th style="padding: 12px; border: 1px solid #ddd;">Warna</th>
                <th style="padding: 12px; border: 1px solid #ddd;">Keterangan</th>
            </tr>
            <tr>
                <td style="padding: 10px; border: 1px solid #ddd;">AgCl</td>
                <td style="padding: 10px; border: 1px solid #ddd;"><span class="precipitate-white">Putih</span></td>
                <td style="padding: 10px; border: 1px solid #ddd;">Larut dalam NH₄OH</td>
            </tr>
            <tr style="background-color: #f9f9f9;">
                <td style="padding: 10px; border: 1px solid #ddd;">PbCl₂</td>
                <td style="padding: 10px; border: 1px solid #ddd;"><span class="precipitate-white">Putih</span></td>
                <td style="padding: 10px; border: 1px solid #ddd;">Larut dalam air panas</td>
            </tr>
            <tr>
                <td style="padding: 10px; border: 1px solid #ddd;">Hg₂Cl₂</td>
                <td style="padding: 10px; border: 1px solid #ddd;"><span class="precipitate-white">Putih</span></td>
                <td style="padding: 10px; border: 1px solid #ddd;">Berubah hitam dengan NH₄OH</td>
            </tr>
            <tr style="background-color: #f9f9f9;">
                <td style="padding: 10px; border: 1px solid #ddd;">PbCrO₄</td>
                <td style="padding: 10px; border: 1px solid #ddd;"><span class="precipitate-yellow">Kuning</span></td>
                <td style="padding: 10px; border: 1px solid #ddd;">Konfirmasi Pb²⁺</td>
            </tr>
            <tr>
                <td style="padding: 10px; border: 1px solid #ddd;">Al(OH)₃</td>
                <td style="padding: 10px; border: 1px solid #ddd;"><span class="precipitate-white">Putih/Gel</span></td>
                <td style="padding: 10px; border: 1px solid #ddd;">Amfoter, larut dalam NaOH berlebih</td>
            </tr>
            <tr style="background-color: #f9f9f9;">
                <td style="padding: 10px; border: 1px solid #ddd;">Fe(OH)₃</td>
                <td style="padding: 10px; border: 1px solid #ddd;"><span style="color: #8D6E63; font-weight: bold;">Coklat/Merah</span></td>
                <td style="padding: 10px; border: 1px solid #ddd;">Tidak larut dalam basa berlebih</td>
            </tr>
            <tr>
                <td style="padding: 10px; border: 1px solid #ddd;">BaCrO₄</td>
                <td style="padding: 10px; border: 1px solid #ddd;"><span class="precipitate-yellow">Kuning</span></td>
                <td style="padding: 10px; border: 1px solid #ddd;">Konfirmasi Ba²⁺</td>
            </tr>
            <tr style="background-color: #f9f9f9;">
                <td style="padding: 10px; border: 1px solid #ddd;">CaC₂O₄</td>
                <td style="padding: 10px; border: 1px solid #ddd;"><span class="precipitate-white">Putih</span></td>
                <td style="padding: 10px; border: 1px solid #ddd;">Konfirmasi Ca²⁺</td>
            </tr>
            <tr>
                <td style="padding: 10px; border: 1px solid #ddd;">SrCO₃</td>
                <td style="padding: 10px; border: 1px solid #ddd;"><span class="precipitate-white">Putih</span></td>
                <td style="padding: 10px; border: 1px solid #ddd;">Terbentuk dalam kondisi panas</td>
            </tr>
            <tr style="background-color: #f9f9f9;">
                <td style="padding: 10px; border: 1px solid #ddd;">[Fe(SCN)]²⁺</td>
                <td style="padding: 10px; border: 1px solid #ddd;"><span class="solution-red">Merah Darah</span></td>
                <td style="padding: 10px; border: 1px solid #ddd;">Konfirmasi Fe³⁺</td>
            </tr>
        </table>
    </div>

    <div class="cation-card" style="margin-top: 20px;">
        <h3>⚗️ Rangkuman Reaksi Kimia</h3>
        <h4>Golongan I:</h4>
        <ul>
            <li>Pb²⁺ + 2Cl⁻ → PbCl₂↓ (Putih) → <strong>H₂O panas</strong> → larut → + K₂CrO₄ → PbCrO₄↓ (Kuning)</li>
            <li>Ag⁺ + Cl⁻ → AgCl↓ (Putih) → <strong>NH₄OH</strong> → [Ag(NH₃)₂]⁺ → <strong>HNO₃</strong> → AgCl↓ (Putih)</li>
            <li>Hg₂²⁺ + 2Cl⁻ → Hg₂Cl₂↓ (Putih) → <strong>NH₄OH</strong> → Hg↓ (Hitam) + Hg(NH₂)Cl↓ (Putih)</li>
        </ul>
        <h4>Golongan II:</h4>
        <ul>
            <li>Al³⁺ + 3OH⁻ → Al(OH)₃↓ (Putih/Gel) → <strong>NaOH berlebih</strong> → [Al(OH)₄]⁻ → <strong>HCl</strong> → Al(OH)₃↓</li>
            <li>Fe³⁺ + 3OH⁻ → Fe(OH)₃↓ (Coklat) → <strong>KSCN</strong> → [Fe(SCN)]²⁺ (Merah Darah)</li>
            <li>Ba²⁺ + CrO₄²⁻ → BaCrO₄↓ (Kuning)</li>
            <li>Ca²⁺ + C₂O₄²⁻ → CaC₂O₄↓ (Putih)</li>
            <li>Sr²⁺ + CO₃²⁻ → SrCO₃↓ (Putih) [panas]</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.sidebar.markdown("---")
st.sidebar.info("""
**Aplikasi Analisis Kation** 
Dibuat untuk pembelajaran kimia analitik

Versi 1.0 | 2026
""")