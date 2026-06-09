const fs = require('fs');
const path = require('path');

const promptDir = path.join(process.cwd(), '.cloudcode');
const promptFile = path.join(promptDir, 'prompt.txt');
const responseFile = path.join(promptDir, 'assistant-response.txt');

if (!fs.existsSync(promptDir)) {
  fs.mkdirSync(promptDir, { recursive: true });
}

if (!fs.existsSync(promptFile)) {
  fs.writeFileSync(promptFile, '');
}

console.log('Watching prompt file:', promptFile);

let lastStat = null;

function readAndPrint() {
  try {
    const content = fs.readFileSync(promptFile, 'utf8');
    console.clear();
    console.log('=== CloudCode Prompt (updated:', new Date().toLocaleTimeString(),') ===\n');
    console.log(content || '[empty]');
    console.log('\n=== End prompt ===');
  } catch (err) {
    console.error('Error reading prompt file:', err.message);
  }
}

// Initial display
readAndPrint();

fs.watchFile(promptFile, { interval: 500 }, (curr, prev) => {
  if (!lastStat || curr.mtimeMs !== prev.mtimeMs) {
    lastStat = curr;
    readAndPrint();
  }
});

// Simple way to write assistant responses back to a response file if needed
process.on('SIGINT', () => {
  console.log('\nStopped watching.');
  process.exit(0);
});
