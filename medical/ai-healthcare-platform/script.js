// AI統合ヘルスケアプラットフォーム - JavaScript

// グローバル変数
let vitalCharts = {};
let isDemoRunning = false;
let demoInterval = null;

// DOM読み込み完了時の初期化
document.addEventListener('DOMContentLoaded', function() {
    initializeNavigation();
    initializeDemo();
    initializeScrollAnimations();
    initializeContactForm();
    initializeVitalCharts();
});

// ナビゲーション初期化
function initializeNavigation() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    const navLinks = document.querySelectorAll('.nav-link');

    // ハンバーガーメニューの切り替え
    hamburger.addEventListener('click', function() {
        hamburger.classList.toggle('active');
        navMenu.classList.toggle('active');
    });

    // ナビゲーションリンククリック時の処理
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetSection = document.getElementById(targetId);
            
            if (targetSection) {
                targetSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
            
            // モバイルメニューを閉じる
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
        });
    });

    // スクロール時のナビゲーションバー背景変更
    window.addEventListener('scroll', function() {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 50) {
            navbar.style.background = 'rgba(255, 255, 255, 0.98)';
            navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.1)';
        } else {
            navbar.style.background = 'rgba(255, 255, 255, 0.95)';
            navbar.style.boxShadow = 'none';
        }
    });
}

// デモ機能初期化
function initializeDemo() {
    const tabButtons = document.querySelectorAll('.tab-button');
    const demoPanels = document.querySelectorAll('.demo-panel');

    // タブ切り替え
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetTab = this.getAttribute('data-tab');
            
            // アクティブタブの切り替え
            tabButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // パネルの切り替え
            demoPanels.forEach(panel => panel.classList.remove('active'));
            document.getElementById(targetTab).classList.add('active');
            
            // デモの開始/停止
            if (targetTab === 'monitoring') {
                startVitalMonitoringDemo();
            } else {
                stopVitalMonitoringDemo();
            }
        });
    });
}

// バイタル監視デモ開始
function startVitalMonitoringDemo() {
    if (isDemoRunning) return;
    
    isDemoRunning = true;
    demoInterval = setInterval(updateVitalSigns, 1000);
    updateVitalSigns(); // 即座に実行
}

// バイタル監視デモ停止
function stopVitalMonitoringDemo() {
    if (demoInterval) {
        clearInterval(demoInterval);
        demoInterval = null;
    }
    isDemoRunning = false;
}

// バイタルサイン更新
function updateVitalSigns() {
    // 心拍数更新
    const heartRateElement = document.getElementById('heart-rate');
    if (heartRateElement) {
        const currentRate = parseInt(heartRateElement.textContent);
        const newRate = Math.max(60, Math.min(100, currentRate + (Math.random() - 0.5) * 4));
        heartRateElement.textContent = Math.round(newRate);
        updateVitalChart('heart-rate-chart', newRate, '#ef4444');
    }

    // 血圧更新
    const bloodPressureElement = document.getElementById('blood-pressure');
    if (bloodPressureElement) {
        const systolic = Math.round(110 + Math.random() * 20);
        const diastolic = Math.round(70 + Math.random() * 10);
        bloodPressureElement.textContent = `${systolic}/${diastolic}`;
        updateVitalChart('blood-pressure-chart', systolic, '#3b82f6');
    }

    // 体温更新
    const temperatureElement = document.getElementById('temperature');
    if (temperatureElement) {
        const currentTemp = parseFloat(temperatureElement.textContent);
        const newTemp = Math.max(36.0, Math.min(37.5, currentTemp + (Math.random() - 0.5) * 0.2));
        temperatureElement.textContent = newTemp.toFixed(1);
        updateVitalChart('temperature-chart', newTemp * 10, '#10b981');
    }
}

// バイタルチャート更新
function updateVitalChart(canvasId, value, color) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;

    // チャートデータの初期化
    if (!vitalCharts[canvasId]) {
        vitalCharts[canvasId] = {
            data: new Array(20).fill(value),
            max: value * 1.2,
            min: value * 0.8
        };
    }

    const chart = vitalCharts[canvasId];
    
    // 新しいデータポイントを追加
    chart.data.push(value);
    chart.data.shift(); // 古いデータを削除
    
    // 範囲を更新
    chart.max = Math.max(chart.max, Math.max(...chart.data) * 1.1);
    chart.min = Math.min(chart.min, Math.min(...chart.data) * 0.9);

    // キャンバスをクリア
    ctx.clearRect(0, 0, width, height);

    // グリッド線を描画
    ctx.strokeStyle = '#e5e7eb';
    ctx.lineWidth = 1;
    for (let i = 0; i <= 4; i++) {
        const y = (height / 4) * i;
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(width, y);
        ctx.stroke();
    }

    // データラインを描画
    ctx.strokeStyle = color;
    ctx.lineWidth = 2;
    ctx.beginPath();
    
    chart.data.forEach((point, index) => {
        const x = (width / (chart.data.length - 1)) * index;
        const y = height - ((point - chart.min) / (chart.max - chart.min)) * height;
        
        if (index === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
    });
    
    ctx.stroke();

    // 最新のデータポイントをハイライト
    const lastIndex = chart.data.length - 1;
    const lastX = (width / (chart.data.length - 1)) * lastIndex;
    const lastY = height - ((chart.data[lastIndex] - chart.min) / (chart.max - chart.min)) * height;
    
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(lastX, lastY, 3, 0, 2 * Math.PI);
    ctx.fill();
}

// バイタルチャート初期化
function initializeVitalCharts() {
    const chartIds = ['heart-rate-chart', 'blood-pressure-chart', 'temperature-chart'];
    
    chartIds.forEach(id => {
        const canvas = document.getElementById(id);
        if (canvas) {
            const ctx = canvas.getContext('2d');
            ctx.clearRect(0, 0, canvas.width, canvas.height);
        }
    });
}

// AI診断実行
function runDiagnosis() {
    const symptomInput = document.getElementById('symptom-input');
    const ageInput = document.getElementById('age-input');
    const resultDiv = document.getElementById('diagnosis-result');
    
    if (!symptomInput.value.trim()) {
        alert('症状を入力してください。');
        return;
    }
    
    if (!ageInput.value) {
        alert('年齢を入力してください。');
        return;
    }
    
    // ローディング表示
    resultDiv.innerHTML = `
        <div class="loading">
            <i class="fas fa-spinner fa-spin"></i>
            <p>AI診断を実行中...</p>
        </div>
    `;
    
    // シミュレーション（実際のAPI呼び出しを想定）
    setTimeout(() => {
        const symptoms = symptomInput.value.toLowerCase();
        const age = parseInt(ageInput.value);
        
        let diagnosis = generateDiagnosis(symptoms, age);
        
        resultDiv.innerHTML = `
            <div class="diagnosis-result-content">
                <h4>AI診断結果</h4>
                <div class="diagnosis-item">
                    <strong>入力症状:</strong> ${symptomInput.value}
                </div>
                <div class="diagnosis-item">
                    <strong>年齢:</strong> ${age}歳
                </div>
                <div class="diagnosis-item">
                    <strong>可能性のある診断:</strong>
                    <ul>
                        ${diagnosis.possibleDiagnoses.map(d => `<li>${d}</li>`).join('')}
                    </ul>
                </div>
                <div class="diagnosis-item">
                    <strong>推奨検査:</strong>
                    <ul>
                        ${diagnosis.recommendedTests.map(t => `<li>${t}</li>`).join('')}
                    </ul>
                </div>
                <div class="diagnosis-item">
                    <strong>治療提案:</strong>
                    <ul>
                        ${diagnosis.treatmentSuggestions.map(t => `<li>${t}</li>`).join('')}
                    </ul>
                </div>
                <div class="confidence-score">
                    <strong>診断信頼度:</strong> ${diagnosis.confidence}%
                </div>
            </div>
        `;
    }, 2000);
}

// 診断結果生成（シミュレーション）
function generateDiagnosis(symptoms, age) {
    const diagnosisMap = {
        '頭痛': {
            possibleDiagnoses: ['緊張性頭痛', '片頭痛', '副鼻腔炎'],
            recommendedTests: ['血圧測定', '神経学的検査', 'CTスキャン'],
            treatmentSuggestions: ['安静', '鎮痛剤', 'ストレス管理'],
            confidence: 85
        },
        '発熱': {
            possibleDiagnoses: ['風邪', 'インフルエンザ', '細菌感染'],
            recommendedTests: ['血液検査', '胸部X線', '尿検査'],
            treatmentSuggestions: ['解熱剤', '水分補給', '安静'],
            confidence: 90
        },
        '胸痛': {
            possibleDiagnoses: ['心筋梗塞', '狭心症', '肋間神経痛'],
            recommendedTests: ['心電図', '心エコー', '血液検査'],
            treatmentSuggestions: ['緊急受診', 'ニトログリセリン', '安静'],
            confidence: 95
        },
        '腹痛': {
            possibleDiagnoses: ['胃腸炎', '虫垂炎', '胆石症'],
            recommendedTests: ['腹部超音波', '血液検査', 'CTスキャン'],
            treatmentSuggestions: ['絶食', '鎮痛剤', '水分補給'],
            confidence: 80
        }
    };
    
    // 症状に基づく診断
    for (let [symptom, diagnosis] of Object.entries(diagnosisMap)) {
        if (symptoms.includes(symptom)) {
            return diagnosis;
        }
    }
    
    // デフォルト診断
    return {
        possibleDiagnoses: ['一般的な体調不良', 'ストレス関連症状'],
        recommendedTests: ['基本的な血液検査', '身体診察'],
        treatmentSuggestions: ['十分な休息', 'バランスの取れた食事', '適度な運動'],
        confidence: 70
    };
}

// 予測医療実行
function runPrediction() {
    const patientIdInput = document.getElementById('patient-id-input');
    const resultDiv = document.getElementById('prediction-result');
    
    if (!patientIdInput.value.trim()) {
        alert('患者IDを入力してください。');
        return;
    }
    
    // ローディング表示
    resultDiv.innerHTML = `
        <div class="loading">
            <i class="fas fa-spinner fa-spin"></i>
            <p>リスク評価を実行中...</p>
        </div>
    `;
    
    // シミュレーション
    setTimeout(() => {
        const patientId = patientIdInput.value;
        const prediction = generateRiskPrediction(patientId);
        
        resultDiv.innerHTML = `
            <div class="prediction-result-content">
                <h4>予測医療リスク評価</h4>
                <div class="prediction-item">
                    <strong>患者ID:</strong> ${patientId}
                </div>
                <div class="prediction-item">
                    <strong>総合リスクスコア:</strong> 
                    <span class="risk-score ${prediction.riskLevel.toLowerCase()}">${prediction.overallRiskScore}/100</span>
                </div>
                <div class="prediction-item">
                    <strong>リスクレベル:</strong> 
                    <span class="risk-level ${prediction.riskLevel.toLowerCase()}">${prediction.riskLevel}</span>
                </div>
                <div class="prediction-item">
                    <strong>疾患リスク予測:</strong>
                    <ul>
                        ${Object.entries(prediction.diseaseRisks).map(([disease, risk]) => 
                            `<li>${disease}: ${risk}%</li>`
                        ).join('')}
                    </ul>
                </div>
                <div class="prediction-item">
                    <strong>予防措置:</strong>
                    <ul>
                        ${prediction.preventiveMeasures.map(measure => `<li>${measure}</li>`).join('')}
                    </ul>
                </div>
                <div class="prediction-item">
                    <strong>監視推奨:</strong>
                    <ul>
                        ${prediction.monitoringRecommendations.map(rec => `<li>${rec}</li>`).join('')}
                    </ul>
                </div>
                <div class="prediction-item">
                    <strong>ライフスタイル推奨:</strong>
                    <ul>
                        ${prediction.lifestyleRecommendations.map(rec => `<li>${rec}</li>`).join('')}
                    </ul>
                </div>
            </div>
        `;
    }, 3000);
}

// リスク予測生成（シミュレーション）
function generateRiskPrediction(patientId) {
    // 患者IDに基づく擬似ランダム生成
    const seed = patientId.split('').reduce((a, b) => a + b.charCodeAt(0), 0);
    const random = (min, max) => min + (Math.sin(seed + Date.now() / 1000) * 0.5 + 0.5) * (max - min);
    
    const overallRiskScore = Math.round(random(20, 80));
    let riskLevel = 'LOW';
    
    if (overallRiskScore > 60) riskLevel = 'HIGH';
    else if (overallRiskScore > 40) riskLevel = 'MEDIUM';
    
    return {
        overallRiskScore,
        riskLevel,
        diseaseRisks: {
            '糖尿病': Math.round(random(5, 30)),
            '高血圧': Math.round(random(10, 40)),
            '心疾患': Math.round(random(3, 25)),
            '脳卒中': Math.round(random(2, 15)),
            'がん': Math.round(random(1, 10))
        },
        preventiveMeasures: [
            '定期的な健康診断',
            '適切な運動習慣',
            'バランスの取れた食事',
            'ストレス管理',
            '十分な睡眠'
        ],
        monitoringRecommendations: [
            '月1回の血圧測定',
            '3ヶ月ごとの血液検査',
            '年1回の心電図検査',
            '体重・BMIの定期的な記録'
        ],
        lifestyleRecommendations: [
            '有酸素運動を週3回以上',
            '塩分摂取量の制限',
            '禁煙・節酒',
            'ストレス解消法の実践',
            '規則正しい生活リズム'
        ]
    };
}

// スクロールアニメーション初期化
function initializeScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate');
            }
        });
    }, observerOptions);
    
    // アニメーション対象要素を監視
    const animateElements = document.querySelectorAll('.feature-card, .spec-category, .contact-item');
    animateElements.forEach(el => {
        el.classList.add('scroll-animate');
        observer.observe(el);
    });
}

// お問い合わせフォーム初期化
function initializeContactForm() {
    const contactForm = document.getElementById('contact-form');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const data = Object.fromEntries(formData);
            
            // フォームバリデーション
            if (!data.name || !data.email || !data.subject || !data.message) {
                alert('すべての項目を入力してください。');
                return;
            }
            
            if (!isValidEmail(data.email)) {
                alert('有効なメールアドレスを入力してください。');
                return;
            }
            
            // 送信処理（シミュレーション）
            const submitButton = this.querySelector('button[type="submit"]');
            const originalText = submitButton.innerHTML;
            
            submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> 送信中...';
            submitButton.disabled = true;
            
            setTimeout(() => {
                alert('お問い合わせありがとうございます。後日担当者よりご連絡いたします。');
                this.reset();
                submitButton.innerHTML = originalText;
                submitButton.disabled = false;
            }, 2000);
        });
    }
}

// メールアドレス検証
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// スムーススクロール
function smoothScrollTo(targetId) {
    const targetElement = document.getElementById(targetId);
    if (targetElement) {
        targetElement.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// ページトップに戻る
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// ウィンドウリサイズ時の処理
window.addEventListener('resize', function() {
    // チャートの再描画
    Object.keys(vitalCharts).forEach(canvasId => {
        const canvas = document.getElementById(canvasId);
        if (canvas) {
            updateVitalChart(canvasId, vitalCharts[canvasId].data[vitalCharts[canvasId].data.length - 1], '#3b82f6');
        }
    });
});

// ページ離脱時のクリーンアップ
window.addEventListener('beforeunload', function() {
    stopVitalMonitoringDemo();
});

// キーボードショートカット
document.addEventListener('keydown', function(e) {
    // Ctrl + Enter でデモ開始/停止
    if (e.ctrlKey && e.key === 'Enter') {
        e.preventDefault();
        if (isDemoRunning) {
            stopVitalMonitoringDemo();
        } else {
            startVitalMonitoringDemo();
        }
    }
    
    // Escape でデモ停止
    if (e.key === 'Escape') {
        stopVitalMonitoringDemo();
    }
});

// パフォーマンス監視
function measurePerformance() {
    if ('performance' in window) {
        window.addEventListener('load', function() {
            setTimeout(() => {
                const perfData = performance.getEntriesByType('navigation')[0];
                console.log('Page Load Time:', perfData.loadEventEnd - perfData.loadEventStart, 'ms');
                console.log('DOM Content Loaded:', perfData.domContentLoadedEventEnd - perfData.domContentLoadedEventStart, 'ms');
            }, 0);
        });
    }
}

// パフォーマンス監視開始
measurePerformance();

// エラーハンドリング
window.addEventListener('error', function(e) {
    console.error('JavaScript Error:', e.error);
    // 本番環境では、エラーをログサービスに送信
});

// 未処理のPromise拒否をキャッチ
window.addEventListener('unhandledrejection', function(e) {
    console.error('Unhandled Promise Rejection:', e.reason);
    // 本番環境では、エラーをログサービスに送信
});

// デバッグモード（開発時のみ）
const DEBUG_MODE = false;

if (DEBUG_MODE) {
    console.log('AI Healthcare Platform - Debug Mode Enabled');
    console.log('Available functions:', {
        startVitalMonitoringDemo,
        stopVitalMonitoringDemo,
        runDiagnosis,
        runPrediction,
        smoothScrollTo,
        scrollToTop
    });
}
