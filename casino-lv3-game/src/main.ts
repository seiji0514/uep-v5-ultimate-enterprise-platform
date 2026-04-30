import "./style.css";

type Suit = "♠" | "♥" | "♦" | "♣";
type Theme = "classic" | "neon" | "vip";
type GameMode = "blackjack" | "poker" | "holdem";
type CpuLevel = "normal" | "hard";
type Street = "preflop" | "flop" | "turn" | "river";
type AiAction = "check" | "call" | "bet" | "raise" | "fold" | "bluff-bet" | "bluff-raise";
type PlayerAction = "fold" | "check" | "call" | "bet" | "raise" | "allin";

interface Card {
  suit: Suit;
  rank: number;
}

interface ReplayFrame {
  label: string;
  detail: string;
  playerCards: Card[];
  dealerCards: Card[];
  communityCards: Card[];
  revealDealer: boolean;
}

interface PokerHandEval {
  rank: number;
  name: string;
  tiebreakers: number[];
}

interface SaveData {
  chips: number;
  wins: number;
  losses: number;
  gamesPlayed: number;
  maxWinStreak: number;
  currentWinStreak: number;
  theme: Theme;
  handStats: Record<string, number>;
  savedReplay: ReplayFrame[];
  aiBattleWins: number;
  aiBattleLosses: number;
  sfxVolume: number;
  bgmVolume: number;
  effectsEnabled: boolean;
  initialChips: number;
}

const STORAGE_KEY = "casino-lv3-local-save-v2";
const INITIAL_SAVE: SaveData = {
  chips: 1000,
  wins: 0,
  losses: 0,
  gamesPlayed: 0,
  maxWinStreak: 0,
  currentWinStreak: 0,
  theme: "classic",
  handStats: {},
  savedReplay: [],
  aiBattleWins: 0,
  aiBattleLosses: 0,
  sfxVolume: 0.8,
  bgmVolume: 0.5,
  effectsEnabled: true,
  initialChips: 1000,
};

let currentMode: GameMode = "blackjack";
let cpuLevel: CpuLevel = "normal";
let deck: Card[] = [];
let playerCards: Card[] = [];
let dealerCards: Card[] = [];
let communityCards: Card[] = [];
let splitHandCards: Card[] = [];
let replayFrames: ReplayFrame[] = [];
let dealerRevealed = false;
let isRoundBusy = false;
let replayIndex = 0;
let replayTimer: number | null = null;
let audioCtx: AudioContext | null = null;
let bgmTimer: number | null = null;
let bgmEnabled = true;
let roundBet = 50;
let aiLog: string[] = [];
let potSize = 0;
let pendingAiAction: AiAction | null = null;
let pendingAiBet = 0;
let playerDecisionResolver: ((action: PlayerAction) => void) | null = null;
let playerStack = 0;
let aiStack = 0;
let playerContribution = 0;
let aiContribution = 0;
let streetCurrentBet = 0;
let playerStreetCommitted = 0;
let aiStreetCommitted = 0;

const save = loadSave();

const app = document.querySelector<HTMLDivElement>("#app");
if (!app) throw new Error("App root not found.");

app.innerHTML = `
  <canvas id="particles"></canvas>
  <div class="table">
    <header class="topbar">
      <h1>Royal Table Ultimate</h1>
      <div class="controls">
        <select id="mode">
          <option value="blackjack">Blackjack+</option>
          <option value="poker">5 Card Poker</option>
          <option value="holdem">Texas Hold'em</option>
        </select>
        <select id="theme">
          <option value="classic">Classic</option>
          <option value="neon">Neon</option>
          <option value="vip">VIP</option>
        </select>
        <select id="cpu-level">
          <option value="normal">CPU: Normal</option>
          <option value="hard">CPU: Hard</option>
        </select>
        <button id="bgm">BGM ON</button>
        <button id="help-toggle">使い方</button>
      </div>
    </header>
    <section id="help-panel" class="help-panel hidden">
      <h3>使い方</h3>
      <ul>
        <li>Modeでゲーム切替: Blackjack+ / 5 Card Poker / Texas Hold'em</li>
        <li>Hold'em: Preflopはプレイヤー先攻、Flop以降はAI先攻</li>
        <li>Hold'em操作: Fold / Check / Call / Bet / Raise / All-in</li>
        <li>Raise額はスライダー調整。再レイズ時は再選択UIが出ます</li>
        <li>Pot / P Stack / AI Stack を見ながら進行します</li>
        <li>リプレイ保存・読込で、直近ハンドの再生が可能です</li>
      </ul>
    </section>
    <section class="stats">
      <div>SFX <input id="sfx-volume" type="range" min="0" max="100" step="5" value="80" /></div>
      <div>BGM <input id="bgm-volume" type="range" min="0" max="100" step="5" value="50" /></div>
      <div>Effects <input id="effects-enabled" type="checkbox" checked /></div>
      <div>Init Chips <input id="initial-chips" type="number" min="500" max="50000" step="100" value="1000" /></div>
      <button id="apply-settings">設定適用</button>
    </section>

    <section class="stats">
      <div>Chips: <strong id="chips"></strong></div>
      <div>Wins: <strong id="wins"></strong></div>
      <div>Losses: <strong id="losses"></strong></div>
      <div>Games: <strong id="games"></strong></div>
      <div>WinStreak: <strong id="streak"></strong></div>
      <div>MaxStreak: <strong id="max-streak"></strong></div>
      <div>AI Win: <strong id="ai-wins"></strong></div>
      <div>AI Loss: <strong id="ai-losses"></strong></div>
      <div>Pot: <strong id="pot-size"></strong></div>
      <div>P Stack: <strong id="player-stack"></strong></div>
      <div>AI Stack: <strong id="ai-stack"></strong></div>
    </section>

    <main class="board">
      <div class="hand">
        <h2>Dealer / CPU</h2>
        <div id="dealer-cards" class="cards"></div>
      </div>
      <div class="hand">
        <h2>Community (Hold'em)</h2>
        <div id="community-cards" class="cards"></div>
      </div>
      <div class="hand">
        <h2>Player</h2>
        <div id="player-cards" class="cards"></div>
      </div>
      <div class="hand">
        <h2>Split Hand (Blackjack)</h2>
        <div id="split-cards" class="cards"></div>
      </div>
      <p id="status">準備完了。配札してください。</p>
    </main>

    <footer class="actions">
      <button id="deal">配札</button>
      <button id="hit">Hit</button>
      <button id="stand">Stand</button>
      <button id="double">Double</button>
      <button id="split">Split</button>
      <button id="insurance">Insurance</button>
      <button id="replay">リプレイ再生</button>
      <button id="save-replay">リプレイ保存</button>
      <button id="load-replay">保存リプレイ読込</button>
      <button id="player-fold">Fold</button>
      <button id="player-check">Check</button>
      <button id="player-call">Call</button>
      <button id="player-bet">Bet</button>
      <button id="player-raise">Raise</button>
      <button id="player-allin">All-in</button>
      <input id="raise-amount" type="range" min="20" max="200" step="10" value="60" />
      <span id="raise-value">Raise: 60</span>
    </footer>

    <section class="panel-grid">
      <section class="replay">
        <h3>ハンド履歴</h3>
        <ul id="replay-list"></ul>
      </section>
      <section class="dashboard">
        <h3>戦績ダッシュボード</h3>
        <ul id="dashboard-list"></ul>
      </section>
      <section class="dashboard">
        <h3>AI対戦ログ</h3>
        <ul id="ai-log-list"></ul>
      </section>
    </section>
  </div>
`;

const modeSelect = selectEl<HTMLSelectElement>("mode");
const themeSelect = selectEl<HTMLSelectElement>("theme");
const cpuSelect = selectEl<HTMLSelectElement>("cpu-level");
const chipsEl = selectEl<HTMLElement>("chips");
const winsEl = selectEl<HTMLElement>("wins");
const lossesEl = selectEl<HTMLElement>("losses");
const gamesEl = selectEl<HTMLElement>("games");
const streakEl = selectEl<HTMLElement>("streak");
const maxStreakEl = selectEl<HTMLElement>("max-streak");
const aiWinsEl = selectEl<HTMLElement>("ai-wins");
const aiLossesEl = selectEl<HTMLElement>("ai-losses");
const potEl = selectEl<HTMLElement>("pot-size");
const playerStackEl = selectEl<HTMLElement>("player-stack");
const aiStackEl = selectEl<HTMLElement>("ai-stack");
const dealerCardsEl = selectEl<HTMLDivElement>("dealer-cards");
const playerCardsEl = selectEl<HTMLDivElement>("player-cards");
const splitCardsEl = selectEl<HTMLDivElement>("split-cards");
const communityCardsEl = selectEl<HTMLDivElement>("community-cards");
const statusEl = selectEl<HTMLElement>("status");
const replayListEl = selectEl<HTMLUListElement>("replay-list");
const dashboardListEl = selectEl<HTMLUListElement>("dashboard-list");
const aiLogListEl = selectEl<HTMLUListElement>("ai-log-list");
const dealBtn = selectEl<HTMLButtonElement>("deal");
const hitBtn = selectEl<HTMLButtonElement>("hit");
const standBtn = selectEl<HTMLButtonElement>("stand");
const doubleBtn = selectEl<HTMLButtonElement>("double");
const splitBtn = selectEl<HTMLButtonElement>("split");
const insuranceBtn = selectEl<HTMLButtonElement>("insurance");
const replayBtn = selectEl<HTMLButtonElement>("replay");
const saveReplayBtn = selectEl<HTMLButtonElement>("save-replay");
const loadReplayBtn = selectEl<HTMLButtonElement>("load-replay");
const bgmBtn = selectEl<HTMLButtonElement>("bgm");
const helpToggleBtn = selectEl<HTMLButtonElement>("help-toggle");
const helpPanelEl = selectEl<HTMLElement>("help-panel");
const playerFoldBtn = selectEl<HTMLButtonElement>("player-fold");
const playerCheckBtn = selectEl<HTMLButtonElement>("player-check");
const playerCallBtn = selectEl<HTMLButtonElement>("player-call");
const playerBetBtn = selectEl<HTMLButtonElement>("player-bet");
const playerRaiseBtn = selectEl<HTMLButtonElement>("player-raise");
const playerAllinBtn = selectEl<HTMLButtonElement>("player-allin");
const raiseAmountInput = selectEl<HTMLInputElement>("raise-amount");
const raiseValueEl = selectEl<HTMLElement>("raise-value");
const sfxVolumeInput = selectEl<HTMLInputElement>("sfx-volume");
const bgmVolumeInput = selectEl<HTMLInputElement>("bgm-volume");
const effectsEnabledInput = selectEl<HTMLInputElement>("effects-enabled");
const initialChipsInput = selectEl<HTMLInputElement>("initial-chips");
const applySettingsBtn = selectEl<HTMLButtonElement>("apply-settings");

themeSelect.value = save.theme;
sfxVolumeInput.value = String(Math.round(save.sfxVolume * 100));
bgmVolumeInput.value = String(Math.round(save.bgmVolume * 100));
effectsEnabledInput.checked = save.effectsEnabled;
initialChipsInput.value = String(save.initialChips);
applyTheme(save.theme);
updateStats();
renderDashboard();
renderAiLog();
refreshActionButtons();

modeSelect.addEventListener("change", () => {
  currentMode = modeSelect.value as GameMode;
  setStatus(`${modeSelect.options[modeSelect.selectedIndex].text} に切替`);
  refreshActionButtons();
});

cpuSelect.addEventListener("change", () => {
  cpuLevel = cpuSelect.value as CpuLevel;
});

themeSelect.addEventListener("change", () => {
  save.theme = themeSelect.value as Theme;
  persistSave();
  applyTheme(save.theme);
});

bgmBtn.addEventListener("click", () => {
  bgmEnabled = !bgmEnabled;
  bgmBtn.textContent = bgmEnabled ? "BGM ON" : "BGM OFF";
  if (bgmEnabled) startBgmLoop();
  else stopBgmLoop();
});
helpToggleBtn.addEventListener("click", () => {
  const nowHidden = helpPanelEl.classList.toggle("hidden");
  helpToggleBtn.textContent = nowHidden ? "使い方" : "使い方を閉じる";
});

dealBtn.addEventListener("click", async () => {
  if (isRoundBusy) return;
  if (currentMode === "blackjack") await startBlackjack();
  if (currentMode === "poker") await startPoker();
  if (currentMode === "holdem") await startHoldem();
});

hitBtn.addEventListener("click", blackjackHit);
standBtn.addEventListener("click", blackjackStand);
doubleBtn.addEventListener("click", blackjackDoubleDown);
splitBtn.addEventListener("click", blackjackSplit);
insuranceBtn.addEventListener("click", blackjackInsurance);
replayBtn.addEventListener("click", playReplay);
playerFoldBtn.addEventListener("click", () => resolvePlayerDecision("fold"));
playerCheckBtn.addEventListener("click", () => resolvePlayerDecision("check"));
playerCallBtn.addEventListener("click", () => resolvePlayerDecision("call"));
playerBetBtn.addEventListener("click", () => resolvePlayerDecision("bet"));
playerRaiseBtn.addEventListener("click", () => resolvePlayerDecision("raise"));
playerAllinBtn.addEventListener("click", () => resolvePlayerDecision("allin"));
raiseAmountInput.addEventListener("input", () => {
  raiseValueEl.textContent = `Raise: ${raiseAmountInput.value}`;
});
applySettingsBtn.addEventListener("click", () => {
  save.sfxVolume = Math.max(0, Math.min(1, Number(sfxVolumeInput.value) / 100));
  save.bgmVolume = Math.max(0, Math.min(1, Number(bgmVolumeInput.value) / 100));
  save.effectsEnabled = effectsEnabledInput.checked;
  save.initialChips = Math.max(500, Math.min(50000, Number(initialChipsInput.value) || 1000));
  persistSave();
  setStatus("設定を適用しました。次ラウンドから反映されます。");
});
saveReplayBtn.addEventListener("click", () => {
  save.savedReplay = replayFrames.map((f) => ({
    ...f,
    playerCards: cloneCards(f.playerCards),
    dealerCards: cloneCards(f.dealerCards),
    communityCards: cloneCards(f.communityCards),
  }));
  persistSave();
  setStatus("リプレイを保存しました。");
});
loadReplayBtn.addEventListener("click", () => {
  if (save.savedReplay.length === 0) {
    setStatus("保存済みリプレイがありません。");
    return;
  }
  replayFrames = save.savedReplay.map((f) => ({
    ...f,
    playerCards: cloneCards(f.playerCards),
    dealerCards: cloneCards(f.dealerCards),
    communityCards: cloneCards(f.communityCards),
  }));
  renderReplay();
  setStatus("保存済みリプレイを読み込みました。");
});

startBgmLoop();
runRuleSanityChecks();

async function startBlackjack(): Promise<void> {
  setRoundBusy(true);
  resetRound();
  dealerRevealed = false;
  deck = createShuffledDeck();
  await dealCardAnimated("player");
  await dealCardAnimated("dealer");
  await dealCardAnimated("player");
  await dealCardAnimated("dealer");
  setStatus("Blackjack+: Hit / Stand / Double / Split / Insurance");
  recordFrame("開始", "Blackjack 開始");
  renderHands(false);
  setRoundBusy(false);
  refreshActionButtons();
}

function blackjackHit(): void {
  if (!isBlackjackPlayable()) return;
  playerCards.push(drawCard());
  playTone(760, 60, 0.03, "square");
  renderHands(false);
  recordFrame("Player", "Hit");
  if (getBlackjackScore(playerCards) > 21) endRound("バースト。敗北。", false, "bust");
}

function blackjackStand(): void {
  if (!isBlackjackPlayable()) return;
  dealerRevealed = true;
  while (getBlackjackScore(dealerCards) < 17) dealerCards.push(drawCard());
  renderHands(true);
  recordFrame("Player", "Stand");
  const playerScore = getBlackjackScore(playerCards);
  const dealerScore = getBlackjackScore(dealerCards);
  if (dealerScore > 21 || playerScore > dealerScore) endRound(`勝利 ${playerScore}-${dealerScore}`, true, "blackjack");
  else if (playerScore < dealerScore) endRound(`敗北 ${playerScore}-${dealerScore}`, false, "blackjack");
  else endRound("引き分け", null, "push");
}

function blackjackDoubleDown(): void {
  if (!isBlackjackPlayable() || save.chips < roundBet) return;
  roundBet *= 2;
  playerCards.push(drawCard());
  playTone(900, 80, 0.04, "triangle");
  recordFrame("Player", "Double Down");
  renderHands(false);
  blackjackStand();
}

function blackjackSplit(): void {
  if (!isBlackjackPlayable() || playerCards.length !== 2) return;
  if (rankValue(playerCards[0]) !== rankValue(playerCards[1]) || save.chips < roundBet) {
    setStatus("Split 条件を満たしていません。");
    return;
  }
  splitHandCards = [playerCards.pop() as Card, drawCard()];
  playerCards.push(drawCard());
  playTone(840, 90, 0.04, "square");
  recordFrame("Player", "Split");
  renderHands(false);
  const hand1 = getBlackjackScore(playerCards);
  const hand2 = getBlackjackScore(splitHandCards);
  setStatus(`Split完了: Main=${hand1}, Split=${hand2}。Standで精算。`);
}

function blackjackInsurance(): void {
  if (!isBlackjackPlayable() || dealerCards.length < 1 || rankValue(dealerCards[0]) !== 14) {
    setStatus("Insurance は Dealer のA表示時のみ。");
    return;
  }
  const insuranceCost = Math.floor(roundBet / 2);
  if (save.chips < insuranceCost) return;
  save.chips -= insuranceCost;
  updateStats();
  const dealerBlackjack = getBlackjackScore(dealerCards) === 21 && dealerCards.length === 2;
  if (dealerBlackjack) {
    save.chips += insuranceCost * 3;
    setStatus("Insurance 成功。");
  } else {
    setStatus("Insurance 失敗。");
  }
  persistSave();
}

async function startPoker(): Promise<void> {
  setRoundBusy(true);
  resetRound();
  dealerRevealed = true;
  pushAiLog("AI: カードを分析中...");
  await sleep(320);
  deck = createShuffledDeck();
  for (let i = 0; i < 5; i += 1) {
    await dealCardAnimated("player");
    await dealCardAnimated("dealer");
  }
  renderHands(true);
  const p = evaluatePoker(playerCards);
  const d = evaluatePoker(dealerCards);
  const cmp = comparePokerHands(p, d);
  pushAiLog(`AI: 私の役は ${d.name}`);
  recordFrame("判定", `Player=${p.name} / Dealer=${d.name}`);
  if (cmp > 0) endRound(`勝利 ${p.name}`, true, p.name);
  else if (cmp < 0) endRound(`敗北 Dealer=${d.name}`, false, d.name);
  else endRound(`引き分け ${p.name}`, null, p.name);
  setRoundBusy(false);
  refreshActionButtons();
}

async function startHoldem(): Promise<void> {
  setRoundBusy(true);
  resetRound();
  dealerRevealed = true;
  pushAiLog("AI: Hold'em モード。対戦開始。");
  deck = createShuffledDeck();
  if (save.chips < 40) {
    save.chips = save.initialChips;
    persistSave();
  }
  playerStack = save.chips;
  aiStack = Math.max(600, save.initialChips);
  commitPlayerToPot(10);
  commitAiToPot(20);
  playerStreetCommitted = 10;
  aiStreetCommitted = 20;
  streetCurrentBet = 20;
  pushAiLog("Blinds: Player SB 10 / AI BB 20");
  updateStats();
  await dealCardAnimated("player");
  await dealCardAnimated("dealer");
  await dealCardAnimated("player");
  await dealCardAnimated("dealer");
  recordFrame("Preflop", "2枚配布");

  if ((await playHoldemStreet("preflop", "Preflop", "player")) !== "continue") return finishHoldemRound();

  for (let i = 0; i < 3; i += 1) {
    communityCards.push(drawCard());
    playTone(640, 50, 0.02, "square");
    renderHands(true);
    await sleep(180);
  }
  resetStreetCommitments();
  recordFrame("Flop", "3枚公開");
  if ((await playHoldemStreet("flop", "Flop", "ai")) !== "continue") return finishHoldemRound();

  communityCards.push(drawCard());
  renderHands(true);
  await sleep(180);
  resetStreetCommitments();
  recordFrame("Turn", "1枚公開");
  if ((await playHoldemStreet("turn", "Turn", "ai")) !== "continue") return finishHoldemRound();

  communityCards.push(drawCard());
  renderHands(true);
  await sleep(180);
  resetStreetCommitments();
  recordFrame("River", "1枚公開");
  if ((await playHoldemStreet("river", "River", "ai")) !== "continue") return finishHoldemRound();
  pushAiLog("AI: ショーダウンに進みます。");

  const pBest = bestFiveFromSeven([...playerCards, ...communityCards]);
  const dBest = bestFiveFromSeven([...dealerCards, ...communityCards]);
  settleSidePotBeforeShowdown();
  const cmp = comparePokerHands(pBest, dBest);
  if (cmp > 0) endRound(`Hold'em勝利 ${pBest.name} (Pot ${potSize})`, true, `holdem_${pBest.name}`);
  else if (cmp < 0) endRound(`Hold'em敗北 CPU=${dBest.name} (Pot ${potSize})`, false, `holdem_${dBest.name}`);
  else endRound("Hold'em 引き分け", null, "holdem_push");
  finishHoldemRound();
}

async function playHoldemStreet(
  street: Street,
  label: "Preflop" | "Flop" | "Turn" | "River",
  firstActor: "player" | "ai",
): Promise<"continue" | "end"> {
  if (firstActor === "player") {
    setStatus(`${label}: 先攻はあなたです (Fold/Check/Call/Bet/Raise/All-in)`);
    refreshActionButtons();
    const openingAction = await waitForPlayerDecision();
    const openingResult = await settleHoldemActions(openingAction, label);
    if (openingResult) return "end";
    if (playerStreetCommitted === aiStreetCommitted) return "continue";
  }

  let turn = 0;
  while (turn < 3) {
    pendingAiAction = decideAiAction(street);
    pendingAiBet = getAiBetAmount(pendingAiAction, street, streetCurrentBet, aiStreetCommitted);
    if (pendingAiAction !== "fold" && pendingAiAction !== "check") {
      const aiPaid = commitAiToPot(pendingAiBet);
      aiStreetCommitted += aiPaid;
      pendingAiBet = aiPaid;
      streetCurrentBet = Math.max(streetCurrentBet, aiStreetCommitted);
    }
    pushAiLog(`AI(${label}): ${toActionText(pendingAiAction)}${pendingAiBet > 0 ? ` ${pendingAiBet}` : ""}`);
    recordFrame(label, `AI=${toActionText(pendingAiAction)} ${pendingAiBet}`);
    if (pendingAiAction === "fold") {
      endRound(`CPUが${label}でフォールド。あなたの勝利。`, true, "cpu_fold");
      return "end";
    }

    setStatus(`${label}: あなたのアクションを選択 (Fold/Check/Call/Bet/Raise/All-in)`);
    refreshActionButtons();
    const playerAction = await waitForPlayerDecision();
    const result = await settleHoldemActions(playerAction, label);
    if (result) return "end";
    if (playerStreetCommitted === aiStreetCommitted) return "continue";
    turn += 1;
  }

  autoMatchStreetGap(label);
  return "continue";
}

async function settleHoldemActions(action: PlayerAction, label: "Preflop" | "Flop" | "Turn" | "River"): Promise<boolean> {
  const toCall = Math.max(0, streetCurrentBet - playerStreetCommitted);
  if (action === "fold") {
    pushAiLog(`Player(${label}): fold`);
    endRound(`あなたが${label}でフォールド。CPUの勝利。`, false, "player_fold");
    return true;
  }

  if (action === "check" && toCall > 0) {
    pushAiLog(`Player(${label}): check失敗 -> fold扱い`);
    endRound(`チェック不可のため${label}でフォールド扱い。`, false, "invalid_check_fold");
    return true;
  }

  if (action === "call") {
    const paid = commitPlayerToPot(toCall);
    playerStreetCommitted += paid;
    pushAiLog(`Player(${label}): call ${paid}`);
    recordFrame(label, `Player=call ${paid}`);
  } else if (action === "bet") {
    if (toCall > 0) {
      endRound(`先にコールが必要なため${label}でフォールド扱い。`, false, "invalid_bet_fold");
      return true;
    }
    const betAmount = Number(raiseAmountInput.value);
    const paid = commitPlayerToPot(betAmount);
    playerStreetCommitted += paid;
    streetCurrentBet = Math.max(streetCurrentBet, playerStreetCommitted);
    pushAiLog(`Player(${label}): bet ${paid}`);
    recordFrame(label, `Player=bet ${paid}`);
    const aiResponds = resolveAiToPlayerRaise(paid);
    if (aiResponds === "fold") {
      endRound(`AIが${label}のベットにフォールド。あなたの勝利。`, true, "ai_fold_to_bet");
      return true;
    }
    if (aiResponds === "call") {
      const aiCall = commitAiToPot(Math.max(0, streetCurrentBet - aiStreetCommitted));
      aiStreetCommitted += aiCall;
      pushAiLog(`AI(${label}): call ${aiCall}`);
      recordFrame(label, `AI=call ${aiCall}`);
    } else {
      const reraise = paid + 30;
      const aiPaid = commitAiToPot(reraise);
      aiStreetCommitted += aiPaid;
      streetCurrentBet = Math.max(streetCurrentBet, aiStreetCommitted);
      pushAiLog(`AI(${label}): re-raise ${aiPaid}`);
      recordFrame(label, `AI=re-raise ${aiPaid}`);
      return await resolvePlayerVsReraise(label);
    }
  } else if (action === "raise") {
    if (toCall <= 0) {
      endRound(`先にベットがないため${label}でレイズ不可。`, false, "invalid_raise_fold");
      return true;
    }
    const raiseAmount = Number(raiseAmountInput.value);
    const paid = commitPlayerToPot(toCall + raiseAmount);
    playerStreetCommitted += paid;
    streetCurrentBet = Math.max(streetCurrentBet, playerStreetCommitted);
    pushAiLog(`Player(${label}): raise ${raiseAmount} (total ${paid})`);
    recordFrame(label, `Player=raise ${paid}`);
    const aiResponds = resolveAiToPlayerRaise(raiseAmount);
    if (aiResponds === "fold") {
      endRound(`AIが${label}のレイズにフォールド。あなたの勝利。`, true, "ai_fold_to_raise");
      return true;
    }
    if (aiResponds === "call") {
      const aiCall = commitAiToPot(Math.max(0, streetCurrentBet - aiStreetCommitted));
      aiStreetCommitted += aiCall;
      pushAiLog(`AI(${label}): call ${aiCall}`);
      recordFrame(label, `AI=call ${aiCall}`);
    } else {
      const reraise = raiseAmount + 40;
      const aiPaid = commitAiToPot(Math.max(0, streetCurrentBet - aiStreetCommitted) + reraise);
      aiStreetCommitted += aiPaid;
      streetCurrentBet = Math.max(streetCurrentBet, aiStreetCommitted);
      pushAiLog(`AI(${label}): re-raise ${aiPaid}`);
      recordFrame(label, `AI=re-raise ${aiPaid}`);
      return await resolvePlayerVsReraise(label);
    }
  } else if (action === "allin") {
    const allinAmount = playerStack;
    if (allinAmount <= 0) {
      endRound("スタック不足のためオールイン不可。", false, "invalid_allin");
      return true;
    }
    const paid = commitPlayerToPot(allinAmount);
    playerStreetCommitted += paid;
    streetCurrentBet = Math.max(streetCurrentBet, playerStreetCommitted);
    pushAiLog(`Player(${label}): all-in ${paid}`);
    recordFrame(label, `Player=all-in ${paid}`);
    const callAmount = Math.min(aiStack, Math.max(0, streetCurrentBet - aiStreetCommitted));
    const aiPaid = commitAiToPot(callAmount);
    aiStreetCommitted += aiPaid;
    pushAiLog(`AI(${label}): call all-in ${aiPaid}`);
    recordFrame(label, `AI=call all-in ${aiPaid}`);
  } else {
    pushAiLog(`Player(${label}): check`);
    recordFrame(label, "Player=check");
  }
  updateStats();
  return false;
}

function waitForPlayerDecision(): Promise<PlayerAction> {
  return new Promise((resolve) => {
    playerDecisionResolver = resolve;
  });
}

function resolvePlayerDecision(action: PlayerAction): void {
  if (!playerDecisionResolver || currentMode !== "holdem" || !isRoundBusy) return;
  const resolver = playerDecisionResolver;
  playerDecisionResolver = null;
  resolver(action);
}

function finishHoldemRound(): void {
  pendingAiAction = null;
  pendingAiBet = 0;
  playerDecisionResolver = null;
  resetStreetCommitments();
  setRoundBusy(false);
  refreshActionButtons();
}

function resetStreetCommitments(): void {
  streetCurrentBet = 0;
  playerStreetCommitted = 0;
  aiStreetCommitted = 0;
}

function decideAiAction(street: Street): AiAction {
  const range = buildAiRange(cpuLevel, street);
  const aiStrength = estimateHoldemStrength(dealerCards, communityCards);
  const pair = dealerCards.length >= 2 && rankValue(dealerCards[0]) === rankValue(dealerCards[1]);
  const suited = dealerCards.length >= 2 && dealerCards[0].suit === dealerCards[1].suit;

  if (pair && aiStrength > range.valueAggressive) return "raise";
  if (suited && aiStrength > range.bluffEntry && Math.random() < range.bluffRate) return "bluff-bet";
  if (aiStrength < range.foldBelow && street !== "preflop") return "fold";
  if (aiStrength > range.valueAggressive) return Math.random() < 0.65 ? "raise" : "bet";
  if (aiStrength > range.valueNormal) return Math.random() < 0.5 ? "bet" : "call";
  if (Math.random() < range.bluffRate) return Math.random() < 0.5 ? "bluff-bet" : "bluff-raise";
  return aiStrength > range.callBelow ? "call" : "check";
}

function buildAiRange(level: CpuLevel, street: Street): {
  foldBelow: number;
  callBelow: number;
  valueNormal: number;
  valueAggressive: number;
  bluffRate: number;
  bluffEntry: number;
} {
  const streetBias = street === "preflop" ? -0.03 : street === "flop" ? 0 : street === "turn" ? 0.03 : 0.05;
  if (level === "hard") {
    return {
      foldBelow: 0.2 + streetBias,
      callBelow: 0.34 + streetBias,
      valueNormal: 0.52 + streetBias,
      valueAggressive: 0.72 + streetBias,
      bluffRate: 0.2,
      bluffEntry: 0.38,
    };
  }
  return {
    foldBelow: 0.24 + streetBias,
    callBelow: 0.39 + streetBias,
    valueNormal: 0.57 + streetBias,
    valueAggressive: 0.77 + streetBias,
    bluffRate: 0.12,
    bluffEntry: 0.43,
  };
}

function getAiBetAmount(
  action: AiAction,
  street: Street,
  currentBet: number,
  aiCommitted: number,
): number {
  const streetBase = street === "preflop" ? 30 : street === "flop" ? 45 : street === "turn" ? 70 : 100;
  if (action === "check" || action === "fold") return 0;
  const toCall = Math.max(0, currentBet - aiCommitted);
  if (action === "call") return toCall;
  if (action === "bet") return currentBet > 0 ? toCall : streetBase;
  if (action === "raise") return toCall + Math.floor(streetBase * 1.1);
  if (action === "bluff-bet") return currentBet > 0 ? toCall + Math.floor(streetBase * 0.4) : Math.floor(streetBase * 0.9);
  const minReraise = Math.max(30, Math.floor(streetBase * 1.2));
  return toCall + minReraise;
}

async function resolvePlayerVsReraise(label: "Preflop" | "Flop" | "Turn" | "River"): Promise<boolean> {
  const toCall = Math.max(0, streetCurrentBet - playerStreetCommitted);
  if (toCall <= 0) return false;
  if (playerStack <= 0) {
    endRound(`あなたが${label}の再レイズに対応不可でフォールド。`, false, "player_fold_reraise");
    return true;
  }

  setStatus(`${label}: AIが再レイズ。再選択してください (Fold/Call/Raise/All-in)`);
  refreshActionButtons();
  const response = await waitForPlayerDecision();
  if (response === "fold") {
    endRound(`あなたが${label}の再レイズにフォールド。`, false, "player_fold_reraise");
    return true;
  }
  if (response === "allin") {
    const paidAllin = commitPlayerToPot(playerStack);
    playerStreetCommitted += paidAllin;
    streetCurrentBet = Math.max(streetCurrentBet, playerStreetCommitted);
    recordFrame(label, `Player=all-in vs reraise ${paidAllin}`);
    pushAiLog(`Player(${label}): all-in vs reraise ${paidAllin}`);
    const aiCall = commitAiToPot(Math.max(0, streetCurrentBet - aiStreetCommitted));
    aiStreetCommitted += aiCall;
    pushAiLog(`AI(${label}): call vs all-in ${aiCall}`);
    recordFrame(label, `AI=call vs all-in ${aiCall}`);
    return false;
  }
  if (response === "raise" && playerStack > toCall) {
    const raiseAmount = Number(raiseAmountInput.value);
    const paidRaise = commitPlayerToPot(Math.min(playerStack, toCall + raiseAmount));
    playerStreetCommitted += paidRaise;
    streetCurrentBet = Math.max(streetCurrentBet, playerStreetCommitted);
    pushAiLog(`Player(${label}): 4-bet ${paidRaise}`);
    recordFrame(label, `Player=4-bet ${paidRaise}`);
    const aiResponds = resolveAiVs4Bet(raiseAmount + 30);
    if (aiResponds === "fold") {
      endRound(`AIが${label}の4ベットにフォールド。あなたの勝利。`, true, "ai_fold_to_4bet");
      return true;
    }
    if (aiResponds === "call") {
      const aiNeed = Math.max(0, streetCurrentBet - aiStreetCommitted);
      const aiPaid = commitAiToPot(aiNeed);
      aiStreetCommitted += aiPaid;
      pushAiLog(`AI(${label}): call ${aiPaid}`);
      recordFrame(label, `AI=call ${aiPaid}`);
      return false;
    }
    const fiveBetExtra = Math.min(aiStack, Math.max(40, raiseAmount + 40));
    const aiPaid = commitAiToPot(Math.max(0, streetCurrentBet - aiStreetCommitted) + fiveBetExtra);
    aiStreetCommitted += aiPaid;
    streetCurrentBet = Math.max(streetCurrentBet, aiStreetCommitted);
    pushAiLog(`AI(${label}): 5-bet ${aiPaid}`);
    recordFrame(label, `AI=5-bet ${aiPaid}`);
    setStatus(`${label}: AIが5bet。Fold/Call/All-in を選択`);
    refreshActionButtons();
    const finalResponse = await waitForPlayerDecision();
    if (finalResponse === "fold") {
      endRound(`あなたが${label}の5betにフォールド。`, false, "player_fold_5bet");
      return true;
    }
    if (finalResponse === "allin") {
      const paidAllin = commitPlayerToPot(playerStack);
      playerStreetCommitted += paidAllin;
      streetCurrentBet = Math.max(streetCurrentBet, playerStreetCommitted);
      pushAiLog(`Player(${label}): all-in vs 5bet ${paidAllin}`);
      recordFrame(label, `Player=all-in vs 5bet ${paidAllin}`);
      const aiCall = commitAiToPot(Math.max(0, streetCurrentBet - aiStreetCommitted));
      aiStreetCommitted += aiCall;
      pushAiLog(`AI(${label}): call vs 5bet all-in ${aiCall}`);
      recordFrame(label, `AI=call vs 5bet all-in ${aiCall}`);
      return false;
    }
    const finalToCall = Math.max(0, streetCurrentBet - playerStreetCommitted);
    const paidCall = commitPlayerToPot(Math.min(playerStack, finalToCall));
    playerStreetCommitted += paidCall;
    pushAiLog(`Player(${label}): call vs 5bet ${paidCall}`);
    recordFrame(label, `Player=call vs 5bet ${paidCall}`);
    if (paidCall < finalToCall) {
      pushAiLog(`Player(${label}): 5bet対応で実質オールイン`);
    }
    return false;
  }

  const paid = commitPlayerToPot(Math.min(playerStack, toCall));
  playerStreetCommitted += paid;
  pushAiLog(`Player(${label}): re-raiseにcall ${paid}`);
  recordFrame(label, `Player=call vs reraise ${paid}`);
  if (paid < toCall) {
    pushAiLog(`Player(${label}): 実質オールインで不足`);
  }
  return false;
}

function autoMatchStreetGap(label: "Preflop" | "Flop" | "Turn" | "River"): void {
  const playerGap = Math.max(0, streetCurrentBet - playerStreetCommitted);
  if (playerGap > 0 && playerStack > 0) {
    const paid = commitPlayerToPot(Math.min(playerStack, playerGap));
    playerStreetCommitted += paid;
    pushAiLog(`Player(${label}): 自動調整call ${paid}`);
    recordFrame(label, `Player=auto-call ${paid}`);
  }
  const aiGap = Math.max(0, streetCurrentBet - aiStreetCommitted);
  if (aiGap > 0 && aiStack > 0) {
    const paid = commitAiToPot(Math.min(aiStack, aiGap));
    aiStreetCommitted += paid;
    pushAiLog(`AI(${label}): 自動調整call ${paid}`);
    recordFrame(label, `AI=auto-call ${paid}`);
  }
  updateStats();
}

function resolveAiToPlayerRaise(raiseAmount: number): "fold" | "call" | "re-raise" {
  const strength = estimateHoldemStrength(dealerCards, communityCards);
  if (strength < 0.34 && raiseAmount >= 80) return "fold";
  if (strength > 0.75 && Math.random() < 0.45) return "re-raise";
  if (Math.random() < 0.1) return "fold";
  return "call";
}

function resolveAiVs4Bet(raiseAmount: number): "fold" | "call" | "five-bet" {
  const strength = estimateHoldemStrength(dealerCards, communityCards);
  if (strength < 0.42 && raiseAmount >= 110) return "fold";
  if (strength > 0.82 && Math.random() < 0.6) return "five-bet";
  if (strength > 0.66 && Math.random() < 0.25) return "five-bet";
  if (Math.random() < 0.08) return "fold";
  return "call";
}

function toActionText(action: AiAction): string {
  if (action === "check") return "チェック";
  if (action === "call") return "コール";
  if (action === "bet") return "ベット";
  if (action === "raise") return "レイズ";
  if (action === "fold") return "フォールド";
  if (action === "bluff-bet") return "ブラフベット";
  return "ブラフレイズ";
}

function endRound(message: string, isWin: boolean | null, handLabel: string): void {
  save.gamesPlayed += 1;
  const holdemSettlement = handLabel.includes("holdem") || handLabel.includes("fold");
  const settlement = holdemSettlement ? Math.max(roundBet, Math.floor(potSize / 2)) : roundBet;
  if (isWin === true) {
    if (holdemSettlement) {
      save.chips += potSize;
    } else {
      save.chips += settlement;
    }
    save.wins += 1;
    save.currentWinStreak += 1;
    save.maxWinStreak = Math.max(save.maxWinStreak, save.currentWinStreak);
    spawnParticles("#ffd166");
    playTone(920, 120, 0.045, "triangle");
    save.aiBattleWins += 1;
    pushAiLog("AI: 今回はあなたの勝ちです。");
  } else if (isWin === false) {
    if (!holdemSettlement) {
      save.chips = Math.max(0, save.chips - settlement);
    }
    save.losses += 1;
    save.currentWinStreak = 0;
    playTone(200, 180, 0.045, "sawtooth");
    save.aiBattleLosses += 1;
    pushAiLog("AI: 私の勝ちです。");
  } else {
    if (holdemSettlement) {
      const playerShare = Math.floor(potSize / 2) + (potSize % 2);
      save.chips += playerShare;
      pushAiLog(`引き分け精算: Player ${playerShare} / AI ${potSize - playerShare}`);
    }
    pushAiLog("AI: いい勝負でした。引き分けです。");
  }
  save.handStats[handLabel] = (save.handStats[handLabel] ?? 0) + 1;
  if (handLabel.includes("holdem")) {
    save.handStats["holdem_total"] = (save.handStats["holdem_total"] ?? 0) + 1;
  }
  persistSave();
  setStatus(message);
  updateStats();
  renderDashboard();
  renderAiLog();
  renderReplay();
  roundBet = 50;
  potSize = 0;
  updateStats();
}

function isBlackjackPlayable(): boolean {
  return currentMode === "blackjack" && !isRoundBusy && playerCards.length > 0;
}

function renderHands(revealDealer: boolean): void {
  dealerCardsEl.innerHTML = dealerCards.map((card, index) => renderCard(card, revealDealer || index !== 1)).join("");
  playerCardsEl.innerHTML = playerCards.map((card) => renderCard(card, true)).join("");
  splitCardsEl.innerHTML = splitHandCards.map((card) => renderCard(card, true)).join("");
  communityCardsEl.innerHTML = communityCards.map((card) => renderCard(card, true)).join("");
}

function renderCard(card: Card, visible: boolean): string {
  if (!visible) return `<div class="card hidden">?</div>`;
  const red = card.suit === "♥" || card.suit === "♦" ? "red" : "";
  return `<div class="card ${red} deal-in">${rankToText(card.rank)}${card.suit}</div>`;
}

function playReplay(): void {
  if (replayFrames.length === 0 || isRoundBusy) return;
  setRoundBusy(true);
  replayIndex = 0;
  if (replayTimer) window.clearInterval(replayTimer);
  replayTimer = window.setInterval(() => {
    const frame = replayFrames[replayIndex];
    if (!frame) {
      if (replayTimer) window.clearInterval(replayTimer);
      replayTimer = null;
      setRoundBusy(false);
      refreshActionButtons();
      renderHands(dealerRevealed);
      setStatus("リプレイ終了");
      return;
    }
    playerCards = cloneCards(frame.playerCards);
    dealerCards = cloneCards(frame.dealerCards);
    communityCards = cloneCards(frame.communityCards);
    renderHands(frame.revealDealer);
    setStatus(`[Replay] ${frame.label} - ${frame.detail}`);
    replayIndex += 1;
  }, 760);
}

function renderReplay(): void {
  replayListEl.innerHTML = replayFrames
    .slice(-10)
    .map((f) => `<li><strong>${f.label}</strong>: ${f.detail}</li>`)
    .join("");
}

function renderDashboard(): void {
  const topHands = Object.entries(save.handStats)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 6);
  dashboardListEl.innerHTML = topHands.map(([name, count]) => `<li>${name}: ${count} 回</li>`).join("");
}

function renderAiLog(): void {
  aiLogListEl.innerHTML = aiLog.slice(-8).map((line) => `<li>${line}</li>`).join("");
}

function updateStats(): void {
  chipsEl.textContent = String(save.chips);
  winsEl.textContent = String(save.wins);
  lossesEl.textContent = String(save.losses);
  gamesEl.textContent = String(save.gamesPlayed);
  streakEl.textContent = String(save.currentWinStreak);
  maxStreakEl.textContent = String(save.maxWinStreak);
  aiWinsEl.textContent = String(save.aiBattleWins);
  aiLossesEl.textContent = String(save.aiBattleLosses);
  potEl.textContent = String(potSize);
  playerStackEl.textContent = String(playerStack);
  aiStackEl.textContent = String(aiStack);
}

function refreshActionButtons(): void {
  const locked = isRoundBusy;
  const waitingHoldemDecision = locked && currentMode === "holdem" && playerDecisionResolver !== null;
  dealBtn.disabled = locked;
  replayBtn.disabled = locked || replayFrames.length === 0;
  saveReplayBtn.disabled = locked || replayFrames.length === 0;
  loadReplayBtn.disabled = locked;
  modeSelect.disabled = locked;
  cpuSelect.disabled = locked;
  const bj = !locked && currentMode === "blackjack" && playerCards.length > 0;
  hitBtn.disabled = !bj;
  standBtn.disabled = !bj;
  doubleBtn.disabled = !bj;
  splitBtn.disabled = !bj;
  insuranceBtn.disabled = !bj;
  playerFoldBtn.disabled = !waitingHoldemDecision;
  const toCall = Math.max(0, streetCurrentBet - playerStreetCommitted);
  playerCheckBtn.disabled = !waitingHoldemDecision || toCall > 0;
  playerCallBtn.disabled = !waitingHoldemDecision || toCall === 0;
  playerBetBtn.disabled = !waitingHoldemDecision || toCall > 0 || playerStack <= 0;
  playerRaiseBtn.disabled = !waitingHoldemDecision || toCall === 0 || playerStack <= toCall;
  playerAllinBtn.disabled = !waitingHoldemDecision || playerStack <= 0;
  raiseAmountInput.disabled = !waitingHoldemDecision;
}

function setRoundBusy(v: boolean): void {
  isRoundBusy = v;
  refreshActionButtons();
}

function resetRound(): void {
  playerCards = [];
  dealerCards = [];
  splitHandCards = [];
  communityCards = [];
  replayFrames = [];
  roundBet = 50;
  potSize = 0;
  playerStack = 0;
  aiStack = 0;
  playerContribution = 0;
  aiContribution = 0;
  aiLog = [];
  pendingAiAction = null;
  pendingAiBet = 0;
  playerDecisionResolver = null;
  renderHands(false);
  renderAiLog();
}

function commitPlayerToPot(amount: number): number {
  const paid = Math.min(Math.max(0, amount), playerStack);
  playerStack -= paid;
  save.chips = Math.max(0, save.chips - paid);
  potSize += paid;
  playerContribution += paid;
  return paid;
}

function commitAiToPot(amount: number): number {
  const paid = Math.min(Math.max(0, amount), aiStack);
  aiStack -= paid;
  potSize += paid;
  aiContribution += paid;
  return paid;
}

function settleSidePotBeforeShowdown(): void {
  const matched = Math.min(playerContribution, aiContribution);
  const mainPot = matched * 2;
  const side = potSize - mainPot;
  if (side <= 0) return;
  if (playerContribution > aiContribution) {
    save.chips += side;
    pushAiLog(`Side Pot ${side}: Playerへ返却`);
  } else if (aiContribution > playerContribution) {
    pushAiLog(`Side Pot ${side}: AIへ返却`);
  }
  potSize = mainPot;
  playerContribution = matched;
  aiContribution = matched;
  updateStats();
}

function recordFrame(label: string, detail: string): void {
  replayFrames.push({
    label,
    detail,
    playerCards: cloneCards(playerCards),
    dealerCards: cloneCards(dealerCards),
    communityCards: cloneCards(communityCards),
    revealDealer: dealerRevealed || currentMode !== "blackjack",
  });
}

async function dealCardAnimated(target: "player" | "dealer"): Promise<void> {
  if (target === "player") playerCards.push(drawCard());
  else dealerCards.push(drawCard());
  playTone(700, 45, 0.024, "square");
  renderHands(target !== "dealer" || dealerRevealed);
  recordFrame("配札", `${target === "player" ? "Player" : "Dealer"} に1枚`);
  await sleep(170);
}

function getBlackjackScore(cards: Card[]): number {
  let total = 0;
  let aces = 0;
  for (const c of cards) {
    if (c.rank === 1) {
      total += 11;
      aces += 1;
    } else if (c.rank >= 10) total += 10;
    else total += c.rank;
  }
  while (total > 21 && aces > 0) {
    total -= 10;
    aces -= 1;
  }
  return total;
}

function bestFiveFromSeven(cards: Card[]): PokerHandEval {
  let best: PokerHandEval = { rank: -1, name: "none", tiebreakers: [] };
  for (let a = 0; a < cards.length - 4; a += 1) {
    for (let b = a + 1; b < cards.length - 3; b += 1) {
      for (let c = b + 1; c < cards.length - 2; c += 1) {
        for (let d = c + 1; d < cards.length - 1; d += 1) {
          for (let e = d + 1; e < cards.length; e += 1) {
            const hand = evaluatePoker([cards[a], cards[b], cards[c], cards[d], cards[e]]);
            if (comparePokerHands(hand, best) > 0) best = hand;
          }
        }
      }
    }
  }
  return best;
}

function evaluatePoker(cards: Card[]): PokerHandEval {
  const counts = new Map<number, number>();
  const suits = new Map<Suit, number>();
  for (const card of cards) {
    const v = rankValue(card);
    counts.set(v, (counts.get(v) ?? 0) + 1);
    suits.set(card.suit, (suits.get(card.suit) ?? 0) + 1);
  }
  const entries = [...counts.entries()].sort((a, b) => (b[1] !== a[1] ? b[1] - a[1] : b[0] - a[0]));
  const values = [...counts.keys()].sort((a, b) => a - b);
  const isFlush = [...suits.values()].some((n) => n === 5);
  const straightHigh = getStraightHigh(values);
  const isStraight = straightHigh > 0;
  const high = [...values].sort((a, b) => b - a);

  if (isFlush && isStraight) return { rank: 8, name: "ストレートフラッシュ", tiebreakers: [straightHigh] };
  if (entries[0][1] === 4) return { rank: 7, name: "フォーカード", tiebreakers: flattenEntries(entries) };
  if (entries[0][1] === 3 && entries[1][1] === 2) return { rank: 6, name: "フルハウス", tiebreakers: flattenEntries(entries) };
  if (isFlush) return { rank: 5, name: "フラッシュ", tiebreakers: high };
  if (isStraight) return { rank: 4, name: "ストレート", tiebreakers: [straightHigh] };
  if (entries[0][1] === 3) return { rank: 3, name: "スリーカード", tiebreakers: flattenEntries(entries) };
  if (entries[0][1] === 2 && entries[1][1] === 2) return { rank: 2, name: "ツーペア", tiebreakers: flattenEntries(entries) };
  if (entries[0][1] === 2) return { rank: 1, name: "ワンペア", tiebreakers: flattenEntries(entries) };
  return { rank: 0, name: "ハイカード", tiebreakers: high };
}

function comparePokerHands(a: PokerHandEval, b: PokerHandEval): number {
  if (a.rank !== b.rank) return a.rank - b.rank;
  for (let i = 0; i < Math.max(a.tiebreakers.length, b.tiebreakers.length); i += 1) {
    const av = a.tiebreakers[i] ?? 0;
    const bv = b.tiebreakers[i] ?? 0;
    if (av !== bv) return av - bv;
  }
  return 0;
}

function createShuffledDeck(): Card[] {
  const suits: Suit[] = ["♠", "♥", "♦", "♣"];
  const cards: Card[] = [];
  for (const s of suits) for (let r = 1; r <= 13; r += 1) cards.push({ suit: s, rank: r });
  for (let i = cards.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1));
    [cards[i], cards[j]] = [cards[j], cards[i]];
  }
  return cards;
}

function drawCard(): Card {
  const c = deck.pop();
  if (!c) throw new Error("Deck empty");
  return c;
}

function flattenEntries(entries: Array<[number, number]>): number[] {
  return entries.flatMap(([rank, count]) => Array.from({ length: count }, () => rank));
}

function getStraightHigh(values: number[]): number {
  const unique = [...new Set(values)].sort((a, b) => a - b);
  if (unique.length !== 5) return 0;
  if (unique[4] - unique[0] === 4) return unique[4];
  return [2, 3, 4, 5, 14].every((v, i) => unique[i] === v) ? 5 : 0;
}

function rankValue(card: Card): number {
  return card.rank === 1 ? 14 : card.rank;
}

function estimateHoldemStrength(hole: Card[], board: Card[]): number {
  const values = hole.map(rankValue).sort((a, b) => b - a);
  let base = 0.2;
  if (values.length >= 2) {
    if (values[0] === values[1]) base += 0.35;
    if (values[0] >= 13) base += 0.18;
    if (values[0] >= 11 && values[1] >= 10) base += 0.12;
    if (hole[0].suit === hole[1].suit) base += 0.08;
  }
  if (board.length >= 3) {
    const best = bestFiveFromSeven([...hole, ...board]);
    base += best.rank * 0.08;
  }
  return Math.max(0, Math.min(1, base));
}

function rankToText(rank: number): string {
  if (rank === 1) return "A";
  if (rank === 11) return "J";
  if (rank === 12) return "Q";
  if (rank === 13) return "K";
  return String(rank);
}

function cloneCards(cards: Card[]): Card[] {
  return cards.map((c) => ({ ...c }));
}

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => window.setTimeout(resolve, ms));
}

function setStatus(text: string): void {
  statusEl.textContent = text;
}

function pushAiLog(text: string): void {
  aiLog.push(text);
  renderAiLog();
}

function applyTheme(theme: Theme): void {
  document.body.dataset.theme = theme;
}

function loadSave(): SaveData {
  const raw = window.localStorage.getItem(STORAGE_KEY);
  if (!raw) return { ...INITIAL_SAVE };
  try {
    const p = JSON.parse(raw) as SaveData;
    return {
      chips: p.chips ?? INITIAL_SAVE.chips,
      wins: p.wins ?? 0,
      losses: p.losses ?? 0,
      gamesPlayed: p.gamesPlayed ?? 0,
      maxWinStreak: p.maxWinStreak ?? 0,
      currentWinStreak: p.currentWinStreak ?? 0,
      theme: p.theme ?? "classic",
      handStats: p.handStats ?? {},
      savedReplay: p.savedReplay ?? [],
      aiBattleWins: p.aiBattleWins ?? 0,
      aiBattleLosses: p.aiBattleLosses ?? 0,
      sfxVolume: p.sfxVolume ?? INITIAL_SAVE.sfxVolume,
      bgmVolume: p.bgmVolume ?? INITIAL_SAVE.bgmVolume,
      effectsEnabled: p.effectsEnabled ?? INITIAL_SAVE.effectsEnabled,
      initialChips: p.initialChips ?? INITIAL_SAVE.initialChips,
    };
  } catch {
    return { ...INITIAL_SAVE };
  }
}

function persistSave(): void {
  window.localStorage.setItem(STORAGE_KEY, JSON.stringify(save));
}

function startBgmLoop(): void {
  if (!bgmEnabled || bgmTimer) return;
  bgmTimer = window.setInterval(() => {
    playTone(262, 140, 0.012 * save.bgmVolume, "triangle");
    window.setTimeout(() => playTone(330, 140, 0.011 * save.bgmVolume, "triangle"), 170);
    window.setTimeout(() => playTone(392, 170, 0.011 * save.bgmVolume, "triangle"), 340);
  }, 1600);
}

function stopBgmLoop(): void {
  if (!bgmTimer) return;
  window.clearInterval(bgmTimer);
  bgmTimer = null;
}

function playTone(freq: number, durationMs: number, gain: number, type: OscillatorType): void {
  if (!save.effectsEnabled) return;
  try {
    audioCtx = audioCtx ?? new AudioContext();
    if (audioCtx.state === "suspended") void audioCtx.resume();
    const osc = audioCtx.createOscillator();
    const amp = audioCtx.createGain();
    osc.type = type;
    osc.frequency.value = freq;
    amp.gain.value = gain * save.sfxVolume;
    osc.connect(amp);
    amp.connect(audioCtx.destination);
    osc.start();
    osc.stop(audioCtx.currentTime + durationMs / 1000);
  } catch {
    // no-op
  }
}

function spawnParticles(color: string): void {
  const canvas = selectEl<HTMLCanvasElement>("particles");
  const ctx = canvas.getContext("2d");
  if (!ctx) return;
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  const particles = Array.from({ length: 100 }, () => ({
    x: window.innerWidth / 2,
    y: window.innerHeight / 3,
    vx: (Math.random() - 0.5) * 12,
    vy: Math.random() * -9 - 4,
    life: 90 + Math.random() * 40,
  }));
  const tick = () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (const p of particles) {
      p.x += p.vx;
      p.y += p.vy;
      p.vy += 0.22;
      p.life -= 1;
      ctx.fillStyle = color;
      ctx.globalAlpha = Math.max(0, p.life / 120);
      ctx.fillRect(p.x, p.y, 7, 7);
    }
    if (particles.some((p) => p.life > 0)) requestAnimationFrame(tick);
    else ctx.clearRect(0, 0, canvas.width, canvas.height);
  };
  tick();
}

function selectEl<T extends HTMLElement>(id: string): T {
  const element = document.getElementById(id);
  if (!element) throw new Error(`Missing element: ${id}`);
  return element as T;
}

function runRuleSanityChecks(): void {
  const sf = evaluatePoker([
    { suit: "♠", rank: 10 },
    { suit: "♠", rank: 11 },
    { suit: "♠", rank: 12 },
    { suit: "♠", rank: 13 },
    { suit: "♠", rank: 1 },
  ]);
  const pair = evaluatePoker([
    { suit: "♠", rank: 2 },
    { suit: "♥", rank: 2 },
    { suit: "♦", rank: 7 },
    { suit: "♣", rank: 10 },
    { suit: "♣", rank: 13 },
  ]);
  if (sf.rank <= pair.rank) {
    pushAiLog("SanityCheck: 役判定に異常があります");
  }
}
