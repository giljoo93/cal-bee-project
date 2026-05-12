import * as API from './api.js';
import * as UI  from './ui.js';

// ── 상태 ──────────────────────────────────────────────
const state = {
    usercode:   localStorage.getItem('usercode') || null,
    grant:      localStorage.getItem('grant')    || null,
    userId:     localStorage.getItem('userId')   || null,
    isLoggedIn: !!localStorage.getItem('usercode')
};

// ── 일정 불러오기 ─────────────────────────────────────
async function loadSchedules() {
    const data = await API.fetchSchedules(state.usercode);
    UI.renderSchedules(data, async (scdNo) => {
        await API.deleteSchedule(scdNo, state.usercode);
        loadSchedules();
    });
}

// ── 로그아웃 ──────────────────────────────────────────
function logout() {
    Object.assign(state, { usercode: null, grant: null, userId: null, isLoggedIn: false });
    localStorage.clear();
    UI.showLoggedOut();
    UI.addMessage('[시스템]', '로그아웃 되었습니다.');
}

// ── 모달 제출 (로그인 / 회원가입) ────────────────────
async function handleModalSubmit() {
    const id   = document.getElementById('modal-id').value.trim();
    const pw   = document.getElementById('modal-pw').value.trim();
    const mode = document.getElementById('modal-submit').dataset.mode;

    if (!id || !pw) {
        UI.setModalMessage('아이디와 비밀번호를 입력하세요.', false);
        return;
    }

    const result = mode === 'signin' ? await API.login(id, pw) : await API.signup(id, pw);

    if (result.success) {
        if (mode === 'signin') {
            Object.assign(state, {
                usercode: result.usercode,
                grant:    result.grant,
                userId:   id,
                isLoggedIn: true
            });
            localStorage.setItem('usercode', result.usercode);
            localStorage.setItem('grant',    result.grant);
            localStorage.setItem('userId',   id);
            UI.closeModal();
            UI.showLoggedIn(id);
            loadSchedules();
            UI.addMessage('[시스템]', `${id}님 환영합니다!`);
        } else {
            UI.setModalMessage(result.message + ' 이제 로그인하세요.', true);
        }
    } else {
        UI.setModalMessage(result.message, false);
    }
}

// ── 일정 등록 ─────────────────────────────────────────
async function handleAddSchedule() {
    const title       = document.getElementById('scd-title').value.trim();
    const date        = document.getElementById('scd-date').value;
    const description = document.getElementById('scd-desc').value.trim();

    if (!title || !date) { alert('제목과 날짜를 입력하세요.'); return; }

    await API.addSchedule(state.usercode, title, date, description);
    document.getElementById('scd-title').value = '';
    document.getElementById('scd-date').value  = '';
    document.getElementById('scd-desc').value  = '';
    loadSchedules();
}

// ── AI 채팅 전송 ──────────────────────────────────────
async function sendMessage() {
    const input    = document.getElementById('chat-input');
    const question = input.value.trim();
    if (!question) return;

    UI.addMessage('나', question);
    input.value = '';

    const chatBox = document.getElementById('chat-box');
    const aiP     = UI.addMessage('cal-bee 🐝', '');

    await API.streamChat(question, (chunk) => {
        aiP.innerHTML    += chunk;
        chatBox.scrollTop = chatBox.scrollHeight;
    });
}

// ── 이벤트 바인딩 ─────────────────────────────────────
document.getElementById('btn-signin').addEventListener('click', (e) => { e.preventDefault(); UI.openModal('signin'); });
document.getElementById('btn-signup').addEventListener('click', (e) => { e.preventDefault(); UI.openModal('signup'); });
document.getElementById('btn-logout').addEventListener('click', (e) => { e.preventDefault(); logout(); });
document.getElementById('modal-close').addEventListener('click', UI.closeModal);
document.getElementById('modal-submit').addEventListener('click', handleModalSubmit);
document.getElementById('btn-send').addEventListener('click', sendMessage);
document.getElementById('btn-add-schedule').addEventListener('click', handleAddSchedule);
document.getElementById('chat-input').addEventListener('keypress', (e) => { if (e.key === 'Enter') sendMessage(); });

// ── 초기화 ────────────────────────────────────────────
if (state.isLoggedIn) {
    UI.showLoggedIn(state.userId);
    loadSchedules();
}
