const mazeContainer = document.getElementById('maze-container');
const trainBtn = document.getElementById('train-btn');
const showPathBtn = document.getElementById('show-path-btn');

// Backend URL (auto detects host)
const BASE_URL = window.location.origin;

let mazeSize = [4, 4]; // default size
let qTable = [];
let rewards = [];
let path = [];
let animationSpeed = 300; // ms per step

// Render maze grid
function renderMaze(rows, cols) {
  mazeContainer.innerHTML = '';
  mazeContainer.style.gridTemplateColumns = `repeat(${cols}, 60px)`;

  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const cell = document.createElement('div');
      cell.id = `cell-${r}-${c}`;
      cell.classList.add('cell');

      if (r === 0 && c === 0) cell.classList.add('start'); // start
      else if (r === rows - 1 && c === cols - 1) cell.classList.add('goal'); // goal
      else if (Math.random() < 0.15) cell.classList.add('wall'); // optional walls

      mazeContainer.appendChild(cell);
    }
  }
}

// Animate agent path
async function animatePath(pathCells) {
  for (const [r, c] of pathCells) {
    const cell = document.getElementById(`cell-${r}-${c}`);
    if (!cell.classList.contains('start') && !cell.classList.contains('goal') && !cell.classList.contains('wall')) {
      cell.classList.add('agent');
      await new Promise(res => setTimeout(res, animationSpeed));
      cell.classList.remove('agent');
      cell.classList.add('visited');
    }
  }
}

// Train agent
trainBtn.addEventListener('click', async () => {
  if (!confirm("Training might take a few seconds. Proceed?")) return;

  trainBtn.disabled = true;
  trainBtn.innerText = 'Training...';

  try {
    const res = await axios.post(`${BASE_URL}/api/train`, {
      grid_size: mazeSize,
      episodes: 500
    });

    qTable = res.data.results.q_table;
    rewards = res.data.results.rewards;
    alert('Training completed!');
  } catch (err) {
    console.error(err);
    alert('Training failed');
  }

  trainBtn.disabled = false;
  trainBtn.innerText = 'Train Agent';
});

// Compute and show path
showPathBtn.addEventListener('click', async () => {
  if (!qTable.length) {
    alert("Please train the agent first!");
    return;
  }

  path = [];
  let [r, c] = [0, 0];
  const rows = mazeSize[0], cols = mazeSize[1];
  const maxSteps = rows * cols * 4; // prevent infinite loops
  let steps = 0;

  while (!(r === rows - 1 && c === cols - 1) && steps < maxSteps) {
    path.push([r, c]);
    const stateIndex = r * cols + c;
    const actions = qTable[stateIndex];
    const maxQ = Math.max(...actions);
    const actionIndex = actions.indexOf(maxQ);

    let moved = false;
    if (actionIndex === 0 && r > 0 && !document.getElementById(`cell-${r-1}-${c}`).classList.contains('wall')) { r--; moved = true; }
    else if (actionIndex === 1 && c < cols - 1 && !document.getElementById(`cell-${r}-${c+1}`).classList.contains('wall')) { c++; moved = true; }
    else if (actionIndex === 2 && r < rows - 1 && !document.getElementById(`cell-${r+1}-${c}`).classList.contains('wall')) { r++; moved = true; }
    else if (actionIndex === 3 && c > 0 && !document.getElementById(`cell-${r}-${c-1}`).classList.contains('wall')) { c--; moved = true; }

    if (!moved) break; // stuck
    steps++;
  }

  path.push([rows - 1, cols - 1]);
  await animatePath(path);
});

// Initialize
renderMaze(mazeSize[0], mazeSize[1]);
