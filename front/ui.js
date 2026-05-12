// ── 채팅 ──────────────────────────────────────────────
export function addMessage(sender, text) {
    const chatBox = document.getElementById('chat-box');
    const p       = document.createElement('p');
    p.innerHTML   = `<strong>${sender}:</strong> ${text}`;
    chatBox.appendChild(p);
    chatBox.scrollTop = chatBox.scrollHeight;
    return p;
}

// ── 로그인/로그아웃 상태 ──────────────────────────────
export function showLoggedIn(userId) {
    document.getElementById('user-status').textContent = `${userId} 님`;
    document.getElementById('btn-signin').classList.add('hidden');
    document.getElementById('btn-signup').classList.add('hidden');
    document.getElementById('btn-logout').classList.remove('hidden');
    document.getElementById('schedule-section').classList.remove('hidden');
}

export function showLoggedOut() {
    document.getElementById('user-status').textContent = '게스트';
    document.getElementById('btn-signin').classList.remove('hidden');
    document.getElementById('btn-signup').classList.remove('hidden');
    document.getElementById('btn-logout').classList.add('hidden');
    document.getElementById('schedule-section').classList.add('hidden');
}

// ── 일정 목록 렌더링 ──────────────────────────────────
export function renderSchedules(data, onDelete) {
    const list  = document.getElementById('schedule-list');
    list.innerHTML = '';

    if (data.length === 0) {
        list.innerHTML = '<p class="no-schedule">등록된 일정이 없습니다.</p>';
        return;
    }

    data.forEach(row => {
        const div       = document.createElement('div');
        div.className   = 'schedule-item';
        div.innerHTML   = `
            <span>${row.SCD_DATE} &nbsp;|&nbsp; <strong>${row.SCD_TITLE}</strong> &nbsp;|&nbsp; ${row.DESCRIPTION || '내용없음'}</span>
            <button data-id="${row.SCD_NO}">삭제</button>
        `;
        div.querySelector('button').addEventListener('click', () => onDelete(row.SCD_NO));
        list.appendChild(div);
    });
}

// ── 모달 ──────────────────────────────────────────────
export function openModal(mode) {
    document.getElementById('modal-title').textContent      = mode === 'signin' ? '로그인' : '회원가입';
    document.getElementById('modal-submit').dataset.mode    = mode;
    document.getElementById('modal-id').value               = '';
    document.getElementById('modal-pw').value               = '';
    document.getElementById('modal-message').textContent    = '';
    document.getElementById('modal-overlay').classList.remove('hidden');
}

export function closeModal() {
    document.getElementById('modal-overlay').classList.add('hidden');
}

export function setModalMessage(message, isSuccess) {
    const el    = document.getElementById('modal-message');
    el.textContent  = message;
    el.style.color  = isSuccess ? 'green' : 'red';
}
