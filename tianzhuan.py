"""任务指令DSL —— 道统算子谱（tianzhuan）
道统出处：天篆讳令，令如程序指令
工程映射：把使命编译成可执行指令序列（带序号与 when 时序，落实紫微时序分册）
生长纪律：本地生长自由，推送远端需治理决议发令。
"""
import datetime

VERBS = {"巡查", "采集", "入库", "上报", "暂停", "恢复", "生长", "体检"}

class Edict:
    """任务指令编译器：多行「动词 对象 [when 时序]」编译为有序指令列表。

    when 字段接受 ISO 8601（日期、日期时间均可），编译期校验合法性；
    指令带序号 seq，render 可还原回文本。
    """

    def describe(self) -> dict:
        return {"name": "tianzhuan", "role": "把使命编译成可执行指令序列",
                "stage": "m1", "verbs": sorted(VERBS)}

    def _parse_when(self, raw, lineno):
        if raw is None:
            return None
        raw = raw.strip()
        if not raw:
            return None
        try:
            datetime.datetime.fromisoformat(raw)
        except ValueError:
            raise ValueError(f"第 {lineno} 行 when 时序不可解析：{raw!r}（须为 ISO 8601）")
        return raw

    def compile(self, text):
        """编译多行指令：每行「动词 对象 [when <ISO时间>]」，保序编号。"""
        instructions = []
        for i, raw in enumerate((text or "").splitlines(), start=1):
            line = raw.strip()
            if not line:
                continue                                  # 空行不生成指令
            parts = line.split()
            if parts[-2] == "when" if len(parts) >= 4 else False:
                verb, obj, when = parts[0], " ".join(parts[1:-2]), self._parse_when(parts[-1], i)
            else:
                verb, obj, when = parts[0], " ".join(parts[1:]), None
            if verb not in VERBS:
                raise ValueError(f"第 {i} 行未知动词：{verb!r}（已知集 {sorted(VERBS)}）")
            if not obj:
                raise ValueError(f"第 {i} 行对象为空：{line!r}")
            instructions.append({"seq": len(instructions) + 1,
                                 "verb": verb, "object": obj, "when": when})
        return instructions

    def render(self, instructions):
        """还原为文本（when 有值则带 when 字段），与编译结果一一对应。"""
        lines = []
        for ins in instructions:
            line = f"{ins['verb']} {ins['object']}"
            if ins.get("when"):
                line += f" when {ins['when']}"
            lines.append(line)
        return "\n".join(lines)
