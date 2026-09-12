import streamlit as st
from bank_backend import Bank

st.set_page_config(page_title="VaultX Bank Manager", page_icon="🏦", layout="centered")

# ----------------------------------------------------------------------
# Styling — brushed steel panels, amber indicator light, and a dark
# digital-readout balance screen.
# ----------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

    :root {
        --steel-0: #1B1D21;
        --steel-1: #26292F;
        --steel-2: #32363D;
        --seam: #40444C;
        --text: #E9E6DD;
        --text-dim: #9B9EA6;
        --amber: #E8A33D;
        --amber-glow: #FFC466;
    }

    .stApp { background-color: #101113; }
    .main { padding-top: 1rem; }
    html, body, [class*="css"] { font-family: 'IBM Plex Mono', Menlo, Consolas, monospace; }

    .vault-header {
        text-align: center;
        padding: 1.6rem 1rem 1.3rem;
        background: linear-gradient(180deg, var(--steel-1), var(--steel-0));
        border: 1px solid var(--seam);
        border-radius: 8px;
        color: var(--text);
        margin-bottom: 1.5rem;
    }
    .vault-header .dial {
        width: 40px; height: 40px;
        margin: 0 auto 12px;
        border-radius: 50%;
        background: radial-gradient(circle at 32% 28%, #3d424b, #1a1c1f 72%);
        border: 1px solid #494e57;
    }
    .vault-header h1 {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        margin-bottom: 0.25rem;
        font-size: 1.5rem;
    }
    .vault-header p {
        margin: 0;
        font-size: 0.75rem;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: var(--text-dim);
    }

    .balance-card {
        background: #0E0F11;
        border: 1px solid var(--seam);
        border-radius: 8px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 1.2rem;
        box-shadow: inset 0 2px 10px rgba(0,0,0,0.6);
    }
    .balance-card .label {
        font-size: 0.7rem;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: var(--text-dim);
    }
    .balance-card .amount {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 2.2rem;
        font-weight: 500;
        margin: 0.25rem 0;
        color: var(--amber-glow);
        text-shadow: 0 0 12px rgba(255,196,102,0.45);
    }
    .balance-card .acc { font-size: 0.85rem; color: var(--text-dim); }

    .stTabs [data-baseweb="tab"] {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
        color: var(--text-dim);
    }
    .stTabs [aria-selected="true"] { color: var(--amber) !important; }

    .stButton>button {
        border-radius: 6px;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
    }
    .stButton>button[kind="primary"] {
        background-color: var(--amber);
        border-color: var(--amber);
        color: #201804;
    }
    .stButton>button[kind="primary"]:hover {
        background-color: var(--amber-glow);
        border-color: var(--amber-glow);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------
# Session state
# ----------------------------------------------------------------------
if "user" not in st.session_state:
    st.session_state.user = None
if "pin" not in st.session_state:
    st.session_state.pin = None


def refresh_user():
    """Re-fetch the logged-in user's latest data after any change."""
    if st.session_state.user:
        acc_no = st.session_state.user.get("accountNo") or st.session_state.user.get("accountNo.")
        fresh = Bank.find_user(acc_no, st.session_state.pin)
        if fresh:
            st.session_state.user = fresh
        else:
            st.session_state.user = None
            st.session_state.pin = None


def logout():
    st.session_state.user = None
    st.session_state.pin = None


# ----------------------------------------------------------------------
# Header
# ----------------------------------------------------------------------
st.markdown(
    """
    <div class="vault-header">
        <div class="dial"></div>
        <h1>VaultX Bank Manager</h1>
        <p>Secure Account Access</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------
# Logged-in dashboard
# ----------------------------------------------------------------------
if st.session_state.user:
    refresh_user()

if st.session_state.user:
    user = st.session_state.user
    acc_no = user.get("accountNo") or user.get("accountNo.")

    st.markdown(
        f"""
        <div class="balance-card">
            <div class="label">Balance on Deposit</div>
            <div class="amount">Rs. {user.get('balance', 0):,}</div>
            <div class="acc">{user['name']} &middot; ACCOUNT {acc_no}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([3, 1])
    with col1:
        st.caption(f"Logged in as **{user['name']}** ({user['email']})")
    with col2:
        st.button("Log Out", on_click=logout, use_container_width=True)

    tab_deposit, tab_withdraw, tab_details, tab_update, tab_delete = st.tabs(
        ["💰 Deposit", "💸 Withdraw", "📄 Details", "✏️ Update", "🗑️ Delete"]
    )

    with tab_deposit:
        with st.form("deposit_form"):
            amount = st.number_input("Amount to deposit", min_value=1, max_value=10000, step=100)
            submitted = st.form_submit_button("Deposit", type="primary")
        if submitted:
            success, msg = Bank.deposit(acc_no, st.session_state.pin, int(amount))
            (st.success if success else st.error)(msg)
            if success:
                refresh_user()
                st.rerun()

    with tab_withdraw:
        with st.form("withdraw_form"):
            amount = st.number_input("Amount to withdraw", min_value=1, step=100)
            submitted = st.form_submit_button("Withdraw", type="primary")
        if submitted:
            success, msg = Bank.withdraw(acc_no, st.session_state.pin, int(amount))
            (st.success if success else st.error)(msg)
            if success:
                refresh_user()
                st.rerun()

    with tab_details:
        st.json(
            {
                "Name": user["name"],
                "Age": user["age"],
                "Email": user["email"],
                "Account Number": acc_no,
                "Balance": f"Rs. {user.get('balance', 0):,}",
            }
        )

    with tab_update:
        st.caption("Leave a field empty to keep it unchanged.")
        with st.form("update_form"):
            new_name = st.text_input("New Name")
            new_email = st.text_input("New Email")
            new_pin = st.text_input("New 4-digit PIN", type="password", max_chars=4)
            submitted = st.form_submit_button("Save Changes", type="primary")
        if submitted:
            success, msg = Bank.update_user(
                acc_no, st.session_state.pin, new_name, new_email, new_pin
            )
            (st.success if success else st.error)(msg)
            if success:
                if new_pin.strip():
                    st.session_state.pin = int(new_pin.strip())
                refresh_user()
                st.rerun()

    with tab_delete:
        st.warning("This action is permanent and cannot be undone.")
        confirm = st.checkbox("I understand, delete my account")
        if st.button("Delete Account", type="primary", disabled=not confirm):
            success, msg = Bank.delete_user(acc_no, st.session_state.pin)
            if success:
                st.success(msg)
                logout()
                st.rerun()
            else:
                st.error(msg)

# ----------------------------------------------------------------------
# Logged-out: Login / Create Account
# ----------------------------------------------------------------------
else:
    tab_login, tab_create = st.tabs(["🔑 Log In", "🆕 Create Account"])

    with tab_login:
        st.subheader("Log in to your account")
        with st.form("login_form"):
            acc_no = st.text_input("Account Number or Email")
            pin = st.text_input("PIN (4 digits)", type="password", max_chars=4)
            submitted = st.form_submit_button("Log In", type="primary")

        if submitted:
            if not acc_no.strip() or not pin.strip():
                st.warning("Please enter both your account identifier and PIN.")
            elif not pin.strip().isdigit():
                st.error("PIN must be numeric.")
            else:
                user = Bank.find_user(acc_no.strip(), int(pin.strip()))
                if user:
                    st.session_state.user = user
                    st.session_state.pin = int(pin.strip())
                    st.rerun()
                else:
                    st.error("No account found with that identifier and PIN.")

    with tab_create:
        st.subheader("Create a new account")
        with st.form("create_form"):
            name = st.text_input("Full Name")
            age = st.number_input("Age", min_value=0, max_value=120, step=1)
            email = st.text_input("Email")
            pin = st.text_input("Choose a 4-digit PIN", type="password", max_chars=4)
            submitted = st.form_submit_button("Create Account", type="primary")

        if submitted:
            user, msg = Bank.create_account(name, int(age), email, pin)
            if user:
                st.success(msg)
                st.info(f"Your account number is **{user.get('accountNo') or user.get('accountNo.')}** — save it, you'll need it to log in!")
                st.balloons()
            else:
                st.error(msg)

st.markdown("---")
st.caption("VaultX Bank Manager · Data is stored locally.")
