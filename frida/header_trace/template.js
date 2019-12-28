var last_thread_id = 0;
var _next_color = 0;

var _palette = [
  // "40",
  "32",
  "33",
  "34",
  "35",
  "36",
  "37"
  // "47",
  // "42",
  // "44",
  // "45",
  // "42",
  // "43",
  // "45;30",
  // "46"
];

function idaAddress(pcAddress, lrAddress, inModule) {
  var baseAdd = Module.findBaseAddress(inModule);
  if (baseAdd > pcAddress) {
    baseAdd = ptr(Module.findBaseAddress("WeChat")).sub(0x100000000);
    inModule = "WeChat";
  }

  var pc = (ptr(pcAddress) - ptr(baseAdd)).toString(16);

  var lr = (ptr(lrAddress) - ptr(baseAdd)).toString(16);

  return inModule + " " + lr + "  " + pc;
}

function bin2Hex(data, len) {
  var data = Memory.readByteArray(data, len);
  var b = new Uint8Array(data);
  var str = "";

  for (var i = 0; i < b.length; i++) {
    str += ("0" + b[i].toString(16)).slice(-2) + "";
  }
  return str;
}

function _print(context, message) {
  // console.log("context.depth " + context.depth);
  var indent = "  | ".repeat(context.depth);

  if (context.threadId !== last_thread_id) {
    last_thread_id = context.threadId;
    _next_color = _next_color + 1;
    // console.log("\n");
  }
  var color = _palette[_next_color % _palette.length];
  console.log(
    "\x1b[" +
    color +
    "m" +
    indent +
    message
  );
}

function hookAddress(idaAddr, inModule) {
  var offset = "0x0";
  if (inModule === undefined || inModule === "WeChat") {
    inModule = "WeChat";
    offset = "0x100000000";
  }
  var baseAddr = Module.findBaseAddress(inModule);
  var method = memAddress(baseAddr, offset, idaAddr);
  return method;
}

function memAddress(memBase, idaBase, idaAddr) {
  var offset = ptr(idaAddr).sub(ptr(idaBase));
  var result = ptr(memBase).add(ptr(offset));
  return result;
}
