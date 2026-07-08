import fs from 'node:fs';
import path from 'node:path';

const collectionPath = process.argv[2] || 'MifosX Fineract API Tests.postman_collection.json';
const resolvedPath = path.resolve(process.cwd(), collectionPath);
const source = fs.readFileSync(resolvedPath, 'utf8');

if (!source.trim()) {
  throw new Error(`Collection file is empty: ${resolvedPath}`);
}

const collection = JSON.parse(source);

function isEmptyScript(script) {
  if (!script || !Object.prototype.hasOwnProperty.call(script, 'exec')) {
    return true;
  }

  const { exec } = script;

  if (typeof exec === 'string') {
    return exec.trim().length === 0;
  }

  if (!Array.isArray(exec)) {
    return true;
  }

  return exec.every((line) => String(line).trim().length === 0);
}

function removeEmptyEvents(node) {
  if (Array.isArray(node.event)) {
    node.event = node.event.filter((event) => !isEmptyScript(event.script));

    if (node.event.length === 0) {
      delete node.event;
    }
  }

  if (Array.isArray(node.item)) {
    node.item.forEach(removeEmptyEvents);
  }
}

removeEmptyEvents(collection);

fs.writeFileSync(resolvedPath, `${JSON.stringify(collection, null, 2)}\n`, 'utf8');
