// ── 인증 ──────────────────────────────────────────────
export async function login(id, pw) {
    const res = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id, pw })
    });
    return res.json();
}

export async function signup(id, pw) {
    const res = await fetch('/api/signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id, pw })
    });
    return res.json();
}

// ── 일정 ──────────────────────────────────────────────
export async function fetchSchedules(usercode) {
    const res = await fetch(`/api/schedules?usercode=${usercode}`);
    return res.json();
}

export async function addSchedule(usercode, title, date, description) {
    const res = await fetch('/api/schedules', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ usercode, title, date, description })
    });
    return res.json();
}

export async function deleteSchedule(scdNo, usercode) {
    const res = await fetch(`/api/schedules/${scdNo}?usercode=${usercode}`, {
        method: 'DELETE'
    });
    return res.json();
}

// ── AI 채팅 ───────────────────────────────────────────
export async function sendChat(usercode, question) {
    const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ usercode, question })
    });
    return res.json();
}
