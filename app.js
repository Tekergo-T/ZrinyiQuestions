/**
 * Zrínyi Ilona Mathematics Competition - Main Application
 * Using sql.js for client-side SQLite database support
 * Single-question navigation with 1-hour timer
 */

// ===== State Management =====
const state = {
    db: null,
    selectedClass: null,
    currentQuiz: [],
    userAnswers: [], // Array of answers, one per question
    currentQuestionIndex: 0,
    timerInterval: null,
    timeRemaining: 60 * 60, // 1 hour in seconds
    startTime: null,
    endTime: null,
    user: null // { name: string, totalScore: number, history: [] }
};

// ===== Constants =====
const TOTAL_QUESTIONS = 25;
const QUIZ_DURATION = 60 * 60; // 1 hour in seconds
const ROBLOX_POINTS_MIN = 105;
const ROBLOX_POINTS_MAX = 125;
const ROBLOX_MINUTES_MIN = 1;
const ROBLOX_MINUTES_MAX = 30;
const ROBLOX_DAILY_MINUTES_CAP = 30;
const DIFFICULTY_DISTRIBUTION = {
    easy: { start: 0, end: 0, count: 0 },
    medium: { start: 1, end: 15, count: 15 },
    hard: { start: 16, end: 25, count: 10 }
};

function pointsToRobloxMinutes(points) {
    if (typeof points !== 'number' || Number.isNaN(points)) return 0;
    if (points < ROBLOX_POINTS_MIN) return 0;
    if (points >= ROBLOX_POINTS_MAX) return ROBLOX_MINUTES_MAX;

    const t = (points - ROBLOX_POINTS_MIN) / (ROBLOX_POINTS_MAX - ROBLOX_POINTS_MIN);
    const raw = ROBLOX_MINUTES_MIN + (ROBLOX_MINUTES_MAX - ROBLOX_MINUTES_MIN) * Math.pow(t, 3);
    return Math.max(0, Math.min(ROBLOX_MINUTES_MAX, Math.round(raw)));
}

function getDailyRobloxMinutes(user, isoDatePrefix) {
    if (!user || !Array.isArray(user.history)) return 0;

    const sum = user.history
        .filter(item => typeof item?.date === 'string' && item.date.startsWith(isoDatePrefix))
        .reduce((acc, item) => {
            const minutes = typeof item.robloxMinutes === 'number'
                ? item.robloxMinutes
                : pointsToRobloxMinutes(item.score);
            return acc + (Number.isFinite(minutes) ? minutes : 0);
        }, 0);

    return Math.max(0, Math.min(ROBLOX_DAILY_MINUTES_CAP, sum));
}

// ===== DOM Elements =====
const elements = {
    loginScreen: document.getElementById('login-screen'),
    loginBtn: document.getElementById('login-btn'),
    usernameInput: document.getElementById('username-input'),
    userInfo: document.getElementById('user-info'),
    userNameDisplay: document.getElementById('user-name-display'),
    rewardStatus: document.getElementById('reward-status'),

    classSelection: document.getElementById('class-selection'),
    quizScreen: document.getElementById('quiz-screen'),
    resultsScreen: document.getElementById('results-screen'),
    selectedClass: document.getElementById('selected-class'),
    timerDisplay: document.getElementById('timer-display'),
    progressFill: document.getElementById('progress-fill'),
    progressCurrent: document.getElementById('progress-current'),
    progressTotal: document.getElementById('progress-total'),
    questionIndicators: document.getElementById('question-indicators'),
    questionContainer: document.getElementById('question-container'),
    currentQuestionNumber: document.getElementById('current-question-number'),
    currentDifficulty: document.getElementById('current-difficulty'),
    currentQuestionText: document.getElementById('current-question-text'),
    currentQuestionImage: document.getElementById('current-question-image'),
    optionsContainer: document.getElementById('options-container'),
    prevQuestion: document.getElementById('prev-question'),
    nextQuestion: document.getElementById('next-question'),
    finishQuiz: document.getElementById('finish-quiz'),
    finalScore: document.getElementById('final-score'),
    timeUsed: document.getElementById('time-used'),
    correctCount: document.getElementById('correct-count'),
    wrongCount: document.getElementById('wrong-count'),
    emptyCount: document.getElementById('empty-count'),
    easyBar: document.getElementById('easy-bar'),
    mediumBar: document.getElementById('medium-bar'),
    hardBar: document.getElementById('hard-bar'),
    easyScore: document.getElementById('easy-score'),
    mediumScore: document.getElementById('medium-score'),
    hardScore: document.getElementById('hard-score'),
    performanceAnalysis: document.getElementById('performance-analysis'),
    answerReviewList: document.getElementById('answer-review-list'),
    newQuiz: document.getElementById('new-quiz'),
    exportPdf: document.getElementById('export-pdf'),
    showJson: document.getElementById('show-json'),
    jsonModal: document.getElementById('json-modal'),
    jsonOutput: document.getElementById('json-output'),
    closeModal: document.getElementById('close-modal'),
    copyJson: document.getElementById('copy-json'),
    quizHistoryContainer: document.getElementById('quiz-history-container'),
    quizHistoryList: document.getElementById('quiz-history-list'),
    clearHistory: document.getElementById('clear-history'),
    showHistoryHeader: document.getElementById('show-history-header'),
    historyModal: document.getElementById('history-modal'),
    closeHistoryModal: document.getElementById('close-history-modal'),
    historyModalList: document.getElementById('history-modal-list'),
    clearHistoryModal: document.getElementById('clear-history-modal'),
    resultsHistoryContainer: document.getElementById('results-history-container'),
    resultsHistoryList: document.getElementById('results-history-list')
};

// ===== Database Initialization =====
async function initDatabase() {
    try {
        const SQL = await initSqlJs({
            locateFile: file => `https://sql.js.org/dist/${file}`
        });

        const savedDb = localStorage.getItem('zrinyi_db');
        if (savedDb) {
            const data = Uint8Array.from(atob(savedDb), c => c.charCodeAt(0));
            state.db = new SQL.Database(data);
            console.log('Loaded database from localStorage');
        } else if (typeof DB_BASE64 !== 'undefined') {
            const data = Uint8Array.from(atob(DB_BASE64), c => c.charCodeAt(0));
            state.db = new SQL.Database(data);
            console.log('Loaded database from embedded base64');
            saveDatabase();
        } else {
            throw new Error('No database source available');
        }

        const result = state.db.exec('SELECT COUNT(*) FROM questions');
        console.log(`Database has ${result[0].values[0][0]} questions`);

        return true;
    } catch (error) {
        console.error('Database initialization error:', error);
        showError('Nem sikerült betölteni az adatbázist. Kérlek frissítsd az oldalt.');
        return false;
    }
}

function saveDatabase() {
    if (state.db) {
        const data = state.db.export();
        let binary = '';
        const len = data.byteLength;
        for (let i = 0; i < len; i++) {
            binary += String.fromCharCode(data[i]);
        }
        const base64 = btoa(binary);
        localStorage.setItem('zrinyi_db', base64);
    }
}

function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.innerHTML = `<p>⚠️ ${message}</p>`;
    errorDiv.style.cssText = 'background: rgba(239, 68, 68, 0.2); border: 1px solid #ef4444; padding: 20px; border-radius: 12px; text-align: center; margin: 20px;';
    document.querySelector('.app-container').prepend(errorDiv);
}

// ===== Initialization =====
async function init() {
    const dbLoaded = await initDatabase();
    if (dbLoaded) {
        setupEventListeners();
        checkLogin();
    }
}

// ===== Login System =====
function checkLogin() {
    const savedUser = localStorage.getItem('zrinyi_user');
    if (savedUser) {
        state.user = JSON.parse(savedUser);
        updateUserDisplay();
        showScreen('class-selection');
    } else {
        populateExistingUsers(); // Show existing users on login page
        showScreen('login-screen');
    }
}

function updateUserDisplay() {
    if (state.user) {
        elements.userInfo.classList.remove('hidden');
        const historyBtn = document.getElementById('show-history-header');
        if (historyBtn) historyBtn.classList.remove('hidden'); // Show history only when logged in

        // Add logout button if not exists
        let logoutBtn = document.getElementById('logout-btn');
        if (!logoutBtn) {
            logoutBtn = document.createElement('button');
            logoutBtn.id = 'logout-btn';
            logoutBtn.className = 'btn-logout';
            logoutBtn.innerHTML = '🚪';
            logoutBtn.title = 'Kijelentkezés';
            logoutBtn.addEventListener('click', showLogoutModal);
            elements.userInfo.appendChild(logoutBtn);
        }

        elements.userNameDisplay.textContent = state.user.name;

        // Roblox minutes: cubic points->minutes, daily cap
        const today = new Date().toISOString().split('T')[0];
        const earnedToday = getDailyRobloxMinutes(state.user, today);
        const remainingToday = Math.max(0, ROBLOX_DAILY_MINUTES_CAP - earnedToday);

        if (earnedToday > 0) {
            elements.rewardStatus.textContent = `🎮 Roblox ma: ${earnedToday}/${ROBLOX_DAILY_MINUTES_CAP} perc`;
            elements.rewardStatus.classList.add('unlocked');
        } else {
            elements.rewardStatus.textContent = `🔒 Roblox (105–125 p → 1–${ROBLOX_MINUTES_MAX} perc; max ${ROBLOX_DAILY_MINUTES_CAP}/nap)`;
            elements.rewardStatus.classList.remove('unlocked');
        }

        // Tooltip with remaining time today
        elements.rewardStatus.title = `Ma még ${remainingToday} perc szerezhető.`;
    } else {
        // Not logged in
        elements.userInfo.classList.add('hidden');
        const historyBtn = document.getElementById('show-history-header');
        if (historyBtn) historyBtn.classList.add('hidden');
    }
}


// ===== Persistence Logic =====
function getUsersDB() {
    return JSON.parse(localStorage.getItem('zrinyi_users_db') || '{}');
}

function saveUserToDB(user) {
    const db = getUsersDB();
    db[user.name] = user;
    localStorage.setItem('zrinyi_users_db', JSON.stringify(db));
}

function login() {
    const name = elements.usernameInput.value.trim();
    if (name) {
        const db = getUsersDB();
        if (db[name]) {
            state.user = db[name]; // Load existing user
        } else {
            state.user = {
                name: name,
                totalScore: 0,
                history: []
            };
        }

        saveUser(); // Saves to current 'zrinyi_user'
        saveUserToDB(state.user); // Persist to DB

        updateUserDisplay();
        showScreen('class-selection');
    }
}

function saveUser() {
    localStorage.setItem('zrinyi_user', JSON.stringify(state.user));
    if (state.user) {
        saveUserToDB(state.user);
    }
}

// Custom Modal instead of confirm/alert
function showLogoutModal() {
    showCustomModal('Biztosan ki szeretnél jelentkezni?', [
        { text: 'Mégsem', class: 'btn-secondary', action: () => closeModal('custom-modal') },
        { text: 'Kijelentkezés', class: 'btn-primary', action: () => performLogout() }
    ]);
}

function performLogout() {
    closeModal('custom-modal');
    state.user = null;
    localStorage.removeItem('zrinyi_user');

    // Clear the logout button that was dynamically added
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) logoutBtn.remove();

    updateUserDisplay();
    populateExistingUsers(); // Show existing users on login page
    showScreen('login-screen');
}

// Populate existing users on login page
function populateExistingUsers() {
    const container = document.getElementById('existing-users-container');
    const list = document.getElementById('existing-users-list');
    if (!container || !list) return;

    const db = getUsersDB();
    const userNames = Object.keys(db);

    if (userNames.length === 0) {
        container.classList.add('hidden');
        return;
    }

    container.classList.remove('hidden');
    list.innerHTML = '';

    userNames.forEach(name => {
        const user = db[name];
        const btn = document.createElement('button');
        btn.className = 'user-select-btn';
        btn.innerHTML = `
            <span class="user-select-name">${name}</span>
            <span class="user-select-stats">${user.totalScore} pont • ${user.history.length} kvíz</span>
        `;
        btn.onclick = () => {
            state.user = user;
            saveUser();
            updateUserDisplay();
            showScreen('class-selection');
        };
        list.appendChild(btn);
    });
}

function showCustomModal(message, buttons) {
    let modal = document.getElementById('custom-modal');
    if (!modal) {
        // Create modal if not exists
        modal = document.createElement('div');
        modal.id = 'custom-modal';
        modal.className = 'modal-overlay';
        document.body.appendChild(modal);
    }

    // Simple HTML with flex actions
    modal.innerHTML = `
        <div class="modal-content glass-card" style="text-align:center; max-width:400px;">
            <p style="font-size:1.2rem; margin-bottom:20px; color:var(--text-primary);">${message}</p>
            <div style="display:flex; gap:15px; justify-content:center;" id="custom-modal-actions">
            </div>
        </div>
    `;

    // Attach buttons via JS to preserve function scope
    const actionContainer = modal.querySelector('#custom-modal-actions');
    buttons.forEach(btn => {
        const b = document.createElement('button');
        b.className = btn.class;
        b.textContent = btn.text;
        b.onclick = btn.action;
        // Styling tweaks if needed
        if (btn.class.includes('btn-primary')) {
            b.style.padding = '10px 20px';
        }
        actionContainer.appendChild(b);
    });

    modal.classList.add('active');
}

function closeModal(id) {
    const modal = document.getElementById(id);
    if (modal) modal.classList.remove('active');
}

function showAlert(message) {
    showCustomModal(message, [
        { text: 'Rendben', class: 'btn-primary', action: () => closeModal('custom-modal') }
    ]);
}

// Ensure chart handles empty or small data nicely
function renderChart(history) {
    const chartContainer = document.getElementById('score-chart');
    if (!chartContainer) return;
    chartContainer.innerHTML = '';

    if (!history || history.length === 0) {
        chartContainer.innerHTML = '<p style="text-align:center; padding-top:80px; color:var(--text-muted)">Nincs még adat</p>';
        return;
    }

    const recent = history.slice(-10);
    const maxScore = 125;

    recent.forEach(h => {
        const wrapper = document.createElement('div');
        wrapper.className = 'chart-bar-wrapper';

        const date = new Date(h.date).toLocaleDateString('hu-HU', { month: 'numeric', day: 'numeric' });
        // Ensure height is visible
        const heightPercent = Math.max(5, (h.score / maxScore) * 100);

        wrapper.innerHTML = `
            <div class="chart-bar" style="height: ${heightPercent}%" data-score="${h.score} pont"></div>
            <span class="chart-date">${date}</span>
        `;

        chartContainer.appendChild(wrapper);
    });
}

// ===== Event Listeners =====
function setupEventListeners() {
    // Login
    elements.loginBtn.addEventListener('click', login);
    elements.usernameInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') login();
    });

    // Class selection buttons

    document.querySelectorAll('.class-btn').forEach(btn => {
        btn.addEventListener('click', () => selectClass(btn.dataset.class));
    });

    // Help Modal
    const showHelpBtn = document.getElementById('show-help-btn');
    const closeHelpModal = document.getElementById('close-help-modal');
    const helpModal = document.getElementById('help-modal');

    if (showHelpBtn) {
        showHelpBtn.addEventListener('click', () => {
            helpModal.classList.remove('hidden');
        });
    }

    if (closeHelpModal) {
        closeHelpModal.addEventListener('click', () => {
            helpModal.classList.add('hidden');
        });
    }

    // Close on outside click
    window.addEventListener('click', (e) => {
        if (e.target === helpModal) {
            helpModal.classList.add('hidden');
        }
    });

    // Navigation buttons
    elements.prevQuestion.addEventListener('click', goToPreviousQuestion);
    // Note: nextQuestion uses onclick (set in updateNavigationButtons) to switch between next/finish
    elements.finishQuiz.addEventListener('click', finishQuiz);

    // New quiz
    elements.newQuiz.addEventListener('click', resetQuiz);

    // PDF export
    elements.exportPdf.addEventListener('click', exportPdf);

    // URL History handling
    window.addEventListener('popstate', (e) => {
        if (e.state && e.state.screen) {
            showScreen(e.state.screen, false);
        } else {
            showScreen('class-selection', false);
        }
    });

    // Clear History (Start Screen)
    if (elements.clearHistory) {
        elements.clearHistory.addEventListener('click', () => {
            showCustomModal('Biztosan törölni szeretnéd az összes korábbi eredményt?', [
                { text: 'Mégsem', class: 'btn-secondary', action: () => closeModal('custom-modal') },
                {
                    text: 'Törlés', class: 'btn-primary', action: () => {
                        closeModal('custom-modal');
                        localStorage.removeItem('zrinyi_history');
                        if (state.user) {
                            state.user.history = [];
                            state.user.totalScore = 0;
                            saveUser();
                        }
                        renderQuizHistory();
                    }
                }
            ]);
        });
    }

    // Global History Modal
    if (elements.showHistoryHeader) {
        console.log('History header button found, attaching listener');
        elements.showHistoryHeader.addEventListener('click', () => {
            console.log('History button clicked');
            renderQuizHistory(); // Refresh data
            if (elements.historyModal) {
                console.log('Opening history modal');
                elements.historyModal.classList.remove('hidden');
            } else {
                console.error('History modal not found!');
            }
        });
    } else {
        console.warn('History header button NOT found in elements');
    }

    if (elements.closeHistoryModal) {
        elements.closeHistoryModal.addEventListener('click', () => {
            elements.historyModal.classList.add('hidden');
        });
    }

    if (elements.clearHistoryModal) {
        elements.clearHistoryModal.addEventListener('click', () => {
            showCustomModal('Biztosan törölni szeretnéd az összes korábbi eredményt?', [
                { text: 'Mégsem', class: 'btn-secondary', action: () => closeModal('custom-modal') },
                {
                    text: 'Törlés', class: 'btn-primary', action: () => {
                        closeModal('custom-modal');
                        localStorage.removeItem('zrinyi_history');
                        if (state.user) {
                            state.user.history = [];
                            state.user.totalScore = 0;
                            saveUser();
                        }
                        renderQuizHistory();
                        elements.historyModal.classList.add('hidden');
                    }
                }
            ]);
        });
    }

    // Close modal on outside click
    elements.historyModal.addEventListener('click', (e) => {
        if (e.target === elements.historyModal) {
            elements.historyModal.classList.add('hidden');
        }
    });

    // JSON export
    elements.showJson.addEventListener('click', showJsonExport);
    elements.closeModal.addEventListener('click', () => elements.jsonModal.classList.add('hidden'));
    elements.copyJson.addEventListener('click', copyJsonToClipboard);

    // Database refresh button
    const refreshDbBtn = document.getElementById('refresh-db-btn');
    if (refreshDbBtn) {
        refreshDbBtn.addEventListener('click', () => {
            showCustomModal('Adatbázis frissítése? Ez újratölti a kérdéseket.', [
                { text: 'Mégsem', class: 'btn-secondary', action: () => closeModal('custom-modal') },
                {
                    text: 'Frissítés', class: 'btn-primary', action: () => {
                        closeModal('custom-modal');
                        localStorage.removeItem('zrinyi_db');
                        location.reload();
                    }
                }
            ]);
        });
    }

    // Close modal on outside click
    elements.jsonModal.addEventListener('click', (e) => {
        if (e.target === elements.jsonModal) {
            elements.jsonModal.classList.add('hidden');
        }
    });

    // Keyboard navigation
    document.addEventListener('keydown', handleKeyboardNav);
}

function handleKeyboardNav(e) {
    if (!elements.quizScreen.classList.contains('active')) return;

    if (e.key === 'ArrowLeft' && state.currentQuestionIndex > 0) {
        goToPreviousQuestion();
    } else if (e.key === 'ArrowRight' && state.currentQuestionIndex < TOTAL_QUESTIONS - 1) {
        goToNextQuestion();
    } else if (['a', 'A', '1'].includes(e.key)) {
        selectAnswer('A');
    } else if (['b', 'B', '2'].includes(e.key)) {
        selectAnswer('B');
    } else if (['c', 'C', '3'].includes(e.key)) {
        selectAnswer('C');
    } else if (['d', 'D', '4'].includes(e.key)) {
        selectAnswer('D');
    } else if (['e', 'E', '5'].includes(e.key)) {
        selectAnswer('E');
    }
}

// ===== Screen Navigation =====
function showScreen(screenId) {
    document.querySelectorAll('.screen').forEach(screen => {
        screen.classList.remove('active');
    });
    document.getElementById(screenId).classList.add('active');
}

// ===== Class Selection =====
function selectClass(classLevel) {
    state.selectedClass = classLevel;
    state.currentQuestionIndex = 0;
    state.userAnswers = new Array(TOTAL_QUESTIONS).fill(null);
    elements.selectedClass.textContent = `${classLevel}. osztály`;

    generateQuiz();
    startTimer();
    showScreen('quiz-screen');
}

// ===== Timer =====
function startTimer() {
    state.timeRemaining = QUIZ_DURATION;
    state.startTime = Date.now();
    updateTimerDisplay();

    state.timerInterval = setInterval(() => {
        state.timeRemaining--;
        updateTimerDisplay();

        if (state.timeRemaining <= 0) {
            finishQuiz();
        }
    }, 1000);
}

function stopTimer() {
    if (state.timerInterval) {
        clearInterval(state.timerInterval);
        state.timerInterval = null;
    }
    state.endTime = Date.now();
}

function updateTimerDisplay() {
    const minutes = Math.floor(state.timeRemaining / 60);
    const seconds = state.timeRemaining % 60;
    const display = `⏱️ ${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    elements.timerDisplay.textContent = display;

    // Update timer styling based on time remaining
    elements.timerDisplay.classList.remove('warning', 'danger');
    if (state.timeRemaining <= 300) { // 5 minutes
        elements.timerDisplay.classList.add('danger');
    } else if (state.timeRemaining <= 600) { // 10 minutes
        elements.timerDisplay.classList.add('warning');
    }
}

// ===== Quiz Generation =====
function generateQuiz() {
    state.currentQuiz = [];

    // We will aim for 5 image questions total (3 Medium, 2 Hard).
    const mediumQuestions = selectQuestionsMixed('medium', DIFFICULTY_DISTRIBUTION.medium.count, 3);
    const hardQuestions = selectQuestionsMixed('hard', DIFFICULTY_DISTRIBUTION.hard.count, 2);

    state.currentQuiz = [...mediumQuestions, ...hardQuestions];

    // Shuffle the global quiz order so images aren't always first or last in their difficulty block
    // (Though they are correctly ordered by difficulty blocks usually? No, the original code kept them in difficulty blocks)
    // The original code was: [...easy, ...medium, ...hard]. We should keep that difficulty progression.
    // But WITHIN each difficulty, we want to shuffle so images aren't always at the top.

    ensureQuizLength();
    incrementShownCounts();

    renderQuestionIndicators();
    renderCurrentQuestion();
}

function selectQuestionsMixed(difficulty, totalCount, imageCount) {
    const textCount = totalCount - imageCount;

    // 1. Get Image Questions
    const imageQ = getQuestionsByType(difficulty, imageCount, true);

    // 2. Get Text Questions
    const textQ = getQuestionsByType(difficulty, textCount, false);

    // 3. Combine and Shuffle
    const combined = [...imageQ, ...textQ];
    return shuffleArray(combined);
}

function getQuestionsByType(difficulty, count, isImage) {
    const imageCondition = isImage ? "(image IS NOT NULL AND image != '')" : "(image IS NULL OR image = '')";
    const query = `
        SELECT id, class, difficulty, question, image, 
               option_a, option_b, option_c, option_d, option_e, 
               correct_answer, shown_count
        FROM questions 
        WHERE class = ? AND difficulty = ? AND ${imageCondition}
        ORDER BY shown_count ASC, RANDOM()
        LIMIT ?
    `;

    const result = state.db.exec(query, [state.selectedClass, difficulty, count]);
    if (!result.length) return [];

    return result[0].values.map(row => ({
        id: row[0],
        class: row[1],
        difficulty: row[2],
        question: row[3],
        image: row[4],
        options: {
            A: row[5],
            B: row[6],
            C: row[7],
            D: row[8],
            E: row[9]
        },
        correct_answer: row[10],
        shown_count: row[11]
    }));
}

function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}

function ensureQuizLength() {
    while (state.currentQuiz.length < TOTAL_QUESTIONS) {
        const query = `
            SELECT id, class, difficulty, question, image, 
                   option_a, option_b, option_c, option_d, option_e, 
                   correct_answer, shown_count
            FROM questions 
            ORDER BY RANDOM()
            LIMIT ?
        `;
        const result = state.db.exec(query, [TOTAL_QUESTIONS - state.currentQuiz.length]);

        if (result.length && result[0].values.length > 0) {
            const additional = result[0].values.map(row => ({
                id: row[0],
                class: row[1],
                difficulty: row[2],
                question: row[3],
                image: row[4],
                options: {
                    A: row[5],
                    B: row[6],
                    C: row[7],
                    D: row[8],
                    E: row[9]
                },
                correct_answer: row[10],
                shown_count: row[11]
            }));
            state.currentQuiz.push(...additional);
        } else {
            break;
        }
    }

    state.currentQuiz = state.currentQuiz.slice(0, TOTAL_QUESTIONS);
}

function incrementShownCounts() {
    const ids = state.currentQuiz.map(q => q.id);
    if (ids.length > 0) {
        const placeholders = ids.map(() => '?').join(',');
        state.db.run(`UPDATE questions SET shown_count = shown_count + 1 WHERE id IN (${placeholders})`, ids);
        saveDatabase();
    }
}

// ===== Question Indicators =====
function renderQuestionIndicators() {
    elements.questionIndicators.innerHTML = '';

    for (let i = 0; i < TOTAL_QUESTIONS; i++) {
        const indicator = document.createElement('div');
        indicator.className = 'question-indicator';
        indicator.textContent = i + 1;
        indicator.dataset.index = i;
        indicator.addEventListener('click', () => goToQuestion(i));
        elements.questionIndicators.appendChild(indicator);
    }

    updateQuestionIndicators();
}

function updateQuestionIndicators() {
    const indicators = elements.questionIndicators.querySelectorAll('.question-indicator');

    indicators.forEach((indicator, index) => {
        indicator.classList.remove('current', 'answered');

        if (index === state.currentQuestionIndex) {
            indicator.classList.add('current');
        }

        if (state.userAnswers[index] !== null) {
            indicator.classList.add('answered');
        }
    });
}

// ===== Question Rendering =====
function renderCurrentQuestion() {
    const index = state.currentQuestionIndex;
    const question = state.currentQuiz[index];
    const questionNumber = index + 1;
    const difficulty = getDifficultyForNumber(questionNumber);

    // Update header
    elements.currentQuestionNumber.textContent = questionNumber;
    elements.currentDifficulty.className = `difficulty-tag ${difficulty}`;
    elements.currentDifficulty.textContent = getDifficultyLabel(difficulty);

    // Update question text
    elements.currentQuestionText.textContent = question.question;

    // Update image if exists
    if (question.image) {
        elements.currentQuestionImage.src = question.image;
        elements.currentQuestionImage.style.display = 'block';
    } else {
        elements.currentQuestionImage.style.display = 'none';
    }

    // Render options
    renderOptions(question, index);

    // Update progress
    updateProgress();

    // Update navigation buttons
    updateNavigationButtons();

    // Update indicators
    updateQuestionIndicators();

    // Animate the question card
    const card = elements.questionContainer.querySelector('.question-card');
    card.classList.remove('active-question');
    void card.offsetWidth; // Trigger reflow
    card.classList.add('active-question');
}

function renderOptions(question, questionIndex) {
    elements.optionsContainer.innerHTML = '';

    ['A', 'B', 'C', 'D', 'E'].forEach(letter => {
        const option = document.createElement('div');
        option.className = 'option';
        option.dataset.letter = letter;

        if (state.userAnswers[questionIndex] === letter) {
            option.classList.add('selected');
        }

        option.innerHTML = `
            <span class="option-letter">${letter}</span>
            <span class="option-text">${question.options[letter]}</span>
        `;

        option.addEventListener('click', () => selectAnswer(letter));
        elements.optionsContainer.appendChild(option);
    });
}

function selectAnswer(letter) {
    state.userAnswers[state.currentQuestionIndex] = letter;

    // Update UI
    elements.optionsContainer.querySelectorAll('.option').forEach(opt => {
        opt.classList.remove('selected');
        if (opt.dataset.letter === letter) {
            opt.classList.add('selected');
        }
    });

    updateQuestionIndicators();
    updateProgress();
}

function getDifficultyForNumber(num) {
    if (num <= 15) return 'medium';
    return 'hard';
}

function getDifficultyLabel(difficulty) {
    const labels = {
        easy: 'Könnyű',
        medium: 'Közepes',
        hard: 'Nehéz'
    };
    return labels[difficulty] || difficulty;
}

// ===== Progress =====
function updateProgress() {
    const answered = state.userAnswers.filter(a => a !== null).length;
    const percentage = ((state.currentQuestionIndex + 1) / TOTAL_QUESTIONS) * 100;

    elements.progressFill.style.width = `${percentage}%`;
    elements.progressCurrent.textContent = state.currentQuestionIndex + 1;
    elements.progressTotal.textContent = TOTAL_QUESTIONS;
}

// ===== Navigation =====
function updateNavigationButtons() {
    elements.prevQuestion.disabled = state.currentQuestionIndex === 0;

    if (state.currentQuestionIndex === TOTAL_QUESTIONS - 1) {
        elements.nextQuestion.textContent = 'Befejezés';
        elements.nextQuestion.onclick = function (e) {
            e.preventDefault();
            finishQuiz();
        };
    } else {
        elements.nextQuestion.textContent = 'Következő →';
        elements.nextQuestion.onclick = function (e) {
            e.preventDefault();
            goToNextQuestion();
        };
    }
}

function goToQuestion(index) {
    if (index >= 0 && index < TOTAL_QUESTIONS) {
        state.currentQuestionIndex = index;
        renderCurrentQuestion();
    }
}

function goToPreviousQuestion() {
    if (state.currentQuestionIndex > 0) {
        state.currentQuestionIndex--;
        renderCurrentQuestion();
    }
}

function goToNextQuestion() {
    if (state.currentQuestionIndex < TOTAL_QUESTIONS - 1) {
        state.currentQuestionIndex++;
        renderCurrentQuestion();
    }
}

// ===== Quiz Completion =====
function finishQuiz() {
    const unanswered = state.userAnswers.filter(a => a === null).length;

    if (unanswered > 0) {
        showCustomModal(`Még ${unanswered} megválaszolatlan kérdés van. Biztosan befejezed?`, [
            { text: 'Vissza', class: 'btn-secondary', action: () => closeModal('custom-modal') },
            {
                text: 'Befejezés', class: 'btn-primary', action: () => {
                    closeModal('custom-modal');
                    completeQuiz();
                }
            }
        ]);
        return;
    }

    completeQuiz();
}

function completeQuiz() {
    stopTimer();
    const results = evaluateAnswers();
    saveQuizHistory(results);
    showScreen('results-screen');
}

function evaluateAnswers() {
    let score = 0;
    let correct = 0;
    let wrong = 0;
    let empty = 0;

    const difficultyResults = {
        easy: { correct: 0, total: DIFFICULTY_DISTRIBUTION.easy.count },
        medium: { correct: 0, total: DIFFICULTY_DISTRIBUTION.medium.count },
        hard: { correct: 0, total: DIFFICULTY_DISTRIBUTION.hard.count }
    };

    // Calculate score based on formula: 4H - R + F = 5H + U
    // H = correct, R = wrong, U = empty, F = total questions (25)
    // score = 5*H + U
    for (let i = 0; i < TOTAL_QUESTIONS; i++) {
        const question = state.currentQuiz[i];
        const userAnswer = state.userAnswers[i];
        const correctAnswer = question.correct_answer;
        const difficulty = getDifficultyForNumber(i + 1);

        if (userAnswer === null) {
            empty++;
            score += 1;
        } else if (userAnswer === correctAnswer) {
            correct++;
            score += 5;
            difficultyResults[difficulty].correct++;
        } else {
            wrong++;
            // 0 points for wrong answer
        }
    }

    // Time used
    const timeUsedSeconds = QUIZ_DURATION - state.timeRemaining;

    displayResults(correct, wrong, empty, score, difficultyResults);

    // Create lightweight quiz data for history (IDs and answers only)
    const quizData = state.currentQuiz.map((q, i) => ({
        id: q.id,
        userAnswer: state.userAnswers[i]
    }));

    return {
        score: score,
        correct: correct,
        wrong: wrong,
        empty: empty,
        total: TOTAL_QUESTIONS,
        date: new Date().toISOString(),
        difficultyResults: difficultyResults,
        timeUsedSeconds: timeUsedSeconds,
        quizData: quizData
    };
}

function displayResults(correct, wrong, empty, score, difficultyResults) {
    elements.finalScore.textContent = score;
    elements.correctCount.textContent = correct;
    elements.wrongCount.textContent = wrong;
    elements.emptyCount.textContent = empty;

    // Time used
    const timeUsedSeconds = QUIZ_DURATION - state.timeRemaining;
    const minutes = Math.floor(timeUsedSeconds / 60);
    const seconds = timeUsedSeconds % 60;
    elements.timeUsed.textContent = `⏱️ Felhasznált idő: ${minutes} perc ${seconds} másodperc`;

    // Difficulty breakdown
    const easyTotal = difficultyResults.easy.total;
    const easyPercent = easyTotal > 0 ? (difficultyResults.easy.correct / easyTotal) * 100 : 0;
    const mediumPercent = (difficultyResults.medium.correct / difficultyResults.medium.total) * 100;
    const hardPercent = (difficultyResults.hard.correct / difficultyResults.hard.total) * 100;

    if (elements.easyBar) {
        elements.easyBar.style.width = `${easyPercent}%`;
        const easyBarParent = elements.easyBar.closest('.difficulty-stat');
        if (easyBarParent && easyTotal === 0) easyBarParent.style.display = 'none';
        else if (easyBarParent) easyBarParent.style.display = 'block';
    }
    elements.mediumBar.style.width = `${mediumPercent}%`;
    elements.hardBar.style.width = `${hardPercent}%`;

    if (elements.easyScore) elements.easyScore.textContent = `${difficultyResults.easy.correct}/${easyTotal}`;
    elements.mediumScore.textContent = `${difficultyResults.medium.correct}/${difficultyResults.medium.total}`;
    elements.hardScore.textContent = `${difficultyResults.hard.correct}/${difficultyResults.hard.total}`;

    const analysis = generatePerformanceAnalysis(correct, difficultyResults);
    elements.performanceAnalysis.innerHTML = `
        <h4>📝 Teljesítmény elemzés</h4>
        <p>${analysis}</p>
    `;

    // Render answer review
    renderAnswerReview();
}

function generatePerformanceAnalysis(correct, difficultyResults) {
    const percentage = (correct / TOTAL_QUESTIONS) * 100;

    let overallAssessment;
    if (percentage >= 90) {
        overallAssessment = 'Kiváló teljesítmény! 🏆';
    } else if (percentage >= 75) {
        overallAssessment = 'Nagyon jó eredmény! 🌟';
    } else if (percentage >= 60) {
        overallAssessment = 'Jó munka! 👍';
    } else if (percentage >= 40) {
        overallAssessment = 'Szorgalmasan gyakorolj tovább! 📚';
    } else {
        overallAssessment = 'Ne add fel, gyakorlással fejlődhetsz! 💪';
    }

    const mediumPercent = (difficultyResults.medium.correct / difficultyResults.medium.total) * 100;
    const hardPercent = (difficultyResults.hard.correct / difficultyResults.hard.total) * 100;

    let focusArea = '';
    if (mediumPercent < 60) {
        focusArea = 'A közepes nehézségű feladatok gyakorlása ajánlott.';
    } else if (hardPercent < 50) {
        focusArea = 'A nehéz feladatokon érdemes dolgozni a további fejlődéshez.';
    } else {
        focusArea = 'Minden nehézségi szinten jól teljesítettél!';
    }

    return `${overallAssessment} ${focusArea} Összesen ${correct} helyes válasz a ${TOTAL_QUESTIONS}-ből (${Math.round(percentage)}%).`;
}

function renderAnswerReview() {
    elements.answerReviewList.innerHTML = '';

    for (let i = 0; i < TOTAL_QUESTIONS; i++) {
        const question = state.currentQuiz[i];
        const userAnswer = state.userAnswers[i];
        const correctAnswer = question.correct_answer;

        let status = 'empty';
        if (userAnswer === null) {
            status = 'empty';
        } else if (userAnswer === correctAnswer) {
            status = 'correct';
        } else {
            status = 'wrong';
        }

        const item = document.createElement('div');
        item.className = `answer-item ${status}`;
        item.dataset.index = i;

        let answerHtml = '';
        if (status === 'empty') {
            answerHtml = `<div class="answers-row"><span class="user-answer">–</span><span class="correct-answer">→${correctAnswer}</span></div>`;
        } else if (status === 'correct') {
            answerHtml = `<div class="answers-row"><span class="user-answer">${userAnswer} ✓</span></div>`;
        } else {
            answerHtml = `<div class="answers-row"><span class="user-answer wrong-text">${userAnswer}</span><span class="correct-answer">→${correctAnswer}</span></div>`;
        }

        item.innerHTML = `
            <span class="q-num">${i + 1}</span>
            ${answerHtml}
        `;

        item.addEventListener('click', () => showQuestionDetail(i));
        elements.answerReviewList.appendChild(item);
    }
}

function showQuestionDetail(index, questionOverride = null, userAnswerOverride = undefined) {
    const question = questionOverride || state.currentQuiz[index];
    const userAnswer = userAnswerOverride !== undefined ? userAnswerOverride : state.userAnswers[index];
    const correctAnswer = question.correct_answer;

    let status = 'empty';
    let statusText = 'Nem válaszolt';
    if (userAnswer === null) {
        status = 'empty';
        statusText = 'Nem válaszolt';
    } else if (userAnswer === correctAnswer) {
        status = 'correct';
        statusText = '✓ Helyes válasz';
    } else {
        status = 'wrong';
        statusText = '✗ Hibás válasz';
    }

    const difficulty = getDifficultyForNumber(index + 1);

    const modal = document.createElement('div');
    modal.className = 'question-detail-modal';
    modal.innerHTML = `
        <div class="question-detail-content">
            <div class="question-detail-header">
                <h3>
                    <span class="question-number">${index + 1}.</span>
                    <span class="difficulty-tag ${difficulty}">${getDifficultyLabel(difficulty)}</span>
                </h3>
                <button class="btn-close" onclick="this.closest('.question-detail-modal').remove()">×</button>
            </div>
            <p class="question-detail-text">${question.question}</p>
            ${question.image ? `<img src="${question.image}" class="question-image" alt="Kérdés ábra">` : ''}
            <div class="question-detail-options">
                ${['A', 'B', 'C', 'D', 'E'].map(letter => {
        let classes = 'detail-option';
        if (letter === userAnswer && userAnswer !== correctAnswer) {
            classes += ' user-selected wrong-option';
        } else if (letter === correctAnswer) {
            classes += ' correct-option';
        } else if (letter === userAnswer) {
            classes += ' user-selected';
        }
        return `<div class="${classes}"><strong>${letter}:</strong> ${question.options[letter]}</div>`;
    }).join('')}
            </div>
            <div class="detail-result ${status}">${statusText}</div>
        </div>
    `;

    modal.addEventListener('click', (e) => {
        if (e.target === modal) modal.remove();
    });

    document.body.appendChild(modal);
}

// ===== Reset =====
function resetQuiz() {
    stopTimer();
    state.selectedClass = null;
    state.currentQuiz = [];
    state.userAnswers = [];
    state.currentQuestionIndex = 0;
    state.timeRemaining = QUIZ_DURATION;
    // Initialize View
    showScreen('class-selection');

    // Render History
    renderQuizHistory();
}

// ===== JSON Export =====
function showJsonExport() {
    const jsonData = generateDatabaseJson();
    elements.jsonOutput.textContent = JSON.stringify(jsonData, null, 2);
    elements.jsonModal.classList.remove('hidden');
}

function generateDatabaseJson() {
    return state.currentQuiz.map((question, index) => ({
        class: question.class,
        number: index + 1,
        difficulty: getDifficultyForNumber(index + 1),
        question: question.question,
        image: question.image || null,
        options: question.options,
        correct_answer: question.correct_answer
    }));
}

function copyJsonToClipboard() {
    const jsonData = generateDatabaseJson();
    const jsonString = JSON.stringify(jsonData, null, 2);

    navigator.clipboard.writeText(jsonString).then(() => {
        elements.copyJson.textContent = 'Másolva! ✓';
        setTimeout(() => {
            elements.copyJson.textContent = 'Másolás';
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy:', err);
        alert('A másolás nem sikerült. Kérlek másold ki manuálisan.');
    });
}

// ===== PDF Export =====
function exportPdf() {
    const printWindow = window.open('', '_blank');

    const questionsHtml = state.currentQuiz.map((question, index) => {
        const questionNumber = index + 1;
        const difficulty = getDifficultyForNumber(questionNumber);
        const diffLabel = getDifficultyLabel(difficulty);

        const optionsHtml = ['A', 'B', 'C', 'D', 'E'].map(letter =>
            `<div class="option"><strong>${letter})</strong> ${question.options[letter]}</div>`
        ).join('');

        return `
            <div class="question">
                <div class="question-header">
                    <span class="q-number">${questionNumber}.</span>
                    <span class="q-difficulty ${difficulty}">${diffLabel}</span>
                </div>
                <p class="q-text">${question.question}</p>
                ${question.image ? `<img src="${question.image}" class="q-image" alt="Ábra">` : ''}
                <div class="options">${optionsHtml}</div>
                <div class="answer-box">Válasz: _____</div>
            </div>
        `;
    }).join('');

    const html = `
<!DOCTYPE html>
<html lang="hu">
<head>
    <meta charset="UTF-8">
    <title>Zrínyi Ilona Matematika Verseny - ${state.selectedClass}. osztály</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { 
            font-family: 'Times New Roman', serif; 
            font-size: 11pt; 
            line-height: 1.4;
            padding: 15mm;
        }
        .header { 
            text-align: center; 
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #333;
        }
        .header h1 { font-size: 16pt; margin-bottom: 5px; }
        .header .subtitle { font-size: 12pt; color: #666; }
        .info-row {
            display: flex;
            justify-content: space-between;
            margin: 15px 0;
            padding: 10px;
            background: #f5f5f5;
        }
        .info-row .field { 
            border-bottom: 1px solid #333; 
            min-width: 150px;
            display: inline-block;
        }
        .questions { display: flex; flex-direction: column; gap: 15px; }
        .question { 
            page-break-inside: avoid;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        .question-header { 
            display: flex; 
            gap: 10px;
            margin-bottom: 8px;
            align-items: center;
        }
        .q-number { font-weight: bold; font-size: 12pt; }
        .q-difficulty { 
            font-size: 9pt; 
            padding: 2px 8px; 
            border-radius: 3px;
            color: white;
        }
        .q-difficulty.easy { background: #22c55e; }
        .q-difficulty.medium { background: #f59e0b; }
        .q-difficulty.hard { background: #ef4444; }
        .q-text { margin-bottom: 10px; }
        .q-image { max-width: 200px; margin: 10px 0; }
        .options { 
            display: flex; 
            flex-wrap: wrap;
            gap: 15px;
            margin-top: 8px;
        }
        .option { 
            white-space: nowrap;
        }
        .answer-box { 
            margin-top: 10px; 
            text-align: right;
            font-weight: bold;
        }
        .footer {
            margin-top: 20px;
            padding-top: 10px;
            border-top: 1px solid #ccc;
            text-align: center;
            font-size: 9pt;
            color: #666;
        }
        @media print {
            body { padding: 10mm; }
            .question { break-inside: avoid; }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Zrínyi Ilona Matematika Verseny</h1>
        <div class="subtitle">${state.selectedClass}. osztály - Gyakorló feladatsor</div>
    </div>
    <div class="info-row">
        <div>Név: <span class="field"></span></div>
        <div>Osztály: <span class="field"></span></div>
        <div>Dátum: <span class="field"></span></div>
    </div>
    <div class="questions">${questionsHtml}</div>
    <div class="footer">
        <p>Időkorlát: 60 perc | Pontozás: Helyes = 5 pont, Rontott = 0 pont, Üres = 1 pont (Max: 125 pont)</p>
    </div>
    <script>window.onload = () => window.print();</script>
</body>
</html>`;

    printWindow.document.write(html);
    printWindow.document.close();
}

// ===== Quiz History =====
// ===== New Elements for Stats/History =====
const statsCard = document.getElementById('stats-card');
if (statsCard) statsCard.addEventListener('click', () => {
    updateStatistics();
    showScreen('stats-screen');
});

// ===== Statistics Logic =====
function updateStatistics() {
    if (!state.user || !state.user.history) return;

    const history = state.user.history;
    const totalQuizzes = history.length;
    const totalPoints = state.user.totalScore;

    // Calculate best score
    let bestScore = 0;
    history.forEach(h => {
        if (h.score > bestScore) bestScore = h.score;
    });

    const avg = totalQuizzes > 0 ? Math.round(totalPoints / totalQuizzes) : 0;

    document.getElementById('total-quizzes').textContent = totalQuizzes;
    document.getElementById('avg-score').textContent = avg;
    document.getElementById('best-score').textContent = bestScore;
    document.getElementById('total-points').textContent = totalPoints;

    renderChart(history);
}

function renderChart(history) {
    const chartContainer = document.getElementById('score-chart');
    if (!chartContainer) return;
    chartContainer.innerHTML = '';

    const recent = history.slice(-10);
    const maxScore = 125;

    recent.forEach(h => {
        const wrapper = document.createElement('div');
        wrapper.className = 'chart-bar-wrapper';

        const date = new Date(h.date).toLocaleDateString('hu-HU', { month: 'numeric', day: 'numeric' });
        const heightPercent = Math.max(5, (h.score / maxScore) * 100);

        wrapper.innerHTML = `
            <div class="chart-bar" style="height: ${heightPercent}%" data-score="${h.score} pont"></div>
            <span class="chart-date">${date}</span>
        `;

        chartContainer.appendChild(wrapper);
    });
}

// ===== Detailed History Review Logic =====
function showHistoryReview(realIndex) {
    if (!state.user || !state.user.history[realIndex]) return;

    const historyItem = state.user.history[realIndex];
    if (!historyItem.quizData) {
        alert("Ehhez a kitöltéshez nincs részletes adat mentve (régi verzió).");
        return;
    }

    showScreen('history-review-screen');

    const date = new Date(historyItem.date).toLocaleDateString('hu-HU', { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' });
    const reviewHeader = document.getElementById('review-header-info');
    reviewHeader.innerHTML = `
        <div>
            <span class="review-label">Időpont</span>
            <span class="review-value">${date}</span>
        </div>
        <div>
            <span class="review-label">Pontszám</span>
            <span class="review-value">${historyItem.score}</span>
        </div>
        <div>
            <span class="review-label">Helyes/Összes</span>
            <span class="review-value">${historyItem.correct} / ${historyItem.total}</span>
        </div>
    `;

    const reviewList = document.getElementById('review-questions-list');
    reviewList.innerHTML = '<div style="text-align:center; padding:20px;">Adatok betöltése...</div>';

    // We need to fetch question texts. This is sync.
    const questionIds = historyItem.quizData.map(q => q.id);
    if (questionIds.length === 0) {
        reviewList.innerHTML = 'Hiba: Nincsenek kérdés azonosítók.';
        return;
    }

    const placeholders = questionIds.map(() => '?').join(',');
    const query = `SELECT id, question, correct_answer, option_a, option_b, option_c, option_d, option_e, image FROM questions WHERE id IN (${placeholders})`;

    try {
        const result = state.db.exec(query, questionIds);

        if (!result.length || !result[0].values) {
            reviewList.innerHTML = 'Hiba: Nem találhatók a kérdések az adatbázisban.';
            return;
        }

        const questionsMap = {};
        result[0].values.forEach(row => {
            questionsMap[row[0]] = {
                text: row[1],
                correct: row[2],
                options: { A: row[3], B: row[4], C: row[5], D: row[6], E: row[7] },
                image: row[8]
            };
        });

        reviewList.innerHTML = '';

        historyItem.quizData.forEach((qItem, idx) => {
            const dbQ = questionsMap[qItem.id];
            if (!dbQ) return;

            const userAns = qItem.userAnswer;
            const correctAns = dbQ.correct;
            const isCorrect = userAns === correctAns;
            const isEmpty = userAns === null;

            // Create compact item matching renderAnswerReview style
            const item = document.createElement('div');
            item.className = `answer-item ${isCorrect ? 'correct' : (isEmpty ? 'empty' : 'wrong')}`;

            // Reconstruct question object for the modal
            const questionObj = {
                question: dbQ.text,
                image: dbQ.image,
                options: dbQ.options,
                correct_answer: dbQ.correct
            };

            let answerHtml = '';
            if (isEmpty) {
                answerHtml = `<div class="answers-row"><span class="user-answer">–</span><span class="correct-answer">→${correctAns}</span></div>`;
            } else if (isCorrect) {
                answerHtml = `<div class="answers-row"><span class="user-answer">${userAns} ✓</span></div>`;
            } else {
                answerHtml = `<div class="answers-row"><span class="user-answer wrong-text">${userAns}</span><span class="correct-answer">→${correctAns}</span></div>`;
            }

            item.innerHTML = `
                <span class="q-num">${idx + 1}</span>
                ${answerHtml}
            `;

            // Open detail modal on click, passing explicit data
            item.addEventListener('click', () => showQuestionDetail(idx, questionObj, userAns));
            reviewList.appendChild(item);
        });

    } catch (e) {
        console.error(e);
        reviewList.innerHTML = 'Hiba történt a részletek betöltése közben.';
    }
}

// ===== Quiz History =====
function saveQuizHistory(results) {
    const historyItem = {
        date: results.date,
        class: state.selectedClass,
        score: results.score,
        correct: results.correct,
        total: results.total,
        quizData: results.quizData,
        robloxMinutes: pointsToRobloxMinutes(results.score)
    };

    let history = JSON.parse(localStorage.getItem('zrinyi_history') || '[]');
    history.unshift(historyItem);
    if (history.length > 50) history.pop();
    localStorage.setItem('zrinyi_history', JSON.stringify(history));

    if (state.user) {
        state.user.history.push(historyItem);
        state.user.totalScore += results.score;
        saveUser();
        updateUserDisplay();
    }

    renderQuizHistory();
}

function renderQuizHistory() {
    const containers = [elements.quizHistoryList, elements.historyModalList].filter(c => c !== null);
    if (containers.length === 0) return;

    let source = [];
    let isUserParams = false;

    if (state.user) {
        source = [...state.user.history].reverse();
        isUserParams = true;
    } else {
        source = JSON.parse(localStorage.getItem('zrinyi_history') || '[]');
    }

    containers.forEach(container => {
        container.innerHTML = '';

        if (source.length === 0) {
            container.innerHTML = '<p style="color:var(--text-muted); text-align:center; padding:20px;">Még nincs előzmény.</p>';
            return;
        }

        source.forEach((entry, reverseIndex) => {
            const realIndex = isUserParams ? (source.length - 1 - reverseIndex) : -1;

            const div = document.createElement('div');
            div.className = 'history-item';
            div.style.cursor = 'pointer';

            const date = new Date(entry.date).toLocaleDateString('hu-HU', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });

            div.innerHTML = `
                <div class="history-header">
                    <span class="history-date">${date}</span>
                    <span class="history-score">${entry.score} pont</span>
                </div>
                <div class="history-details">
                    <span>${entry.correct}/${entry.total} helyes</span>
                    ${isUserParams && entry.quizData ? '<span style="font-size:0.8em; color:var(--accent-primary)">Részletek »</span>' : ''}
                </div>
            `;

            div.addEventListener('click', () => {
                if (isUserParams && entry.quizData) {
                    elements.historyModal.classList.add('hidden'); // Close modal if open
                    showHistoryReview(realIndex);
                }
            });

            container.appendChild(div);
        });
    });
}

function generateHistoryHtml(history) { }

// ===== Start Application =====
document.addEventListener('DOMContentLoaded', init);

