import unittest
from tianzhuan import Edict

class T(unittest.TestCase):
    def test_multiline_compile_preserves_order(self):
        e = Edict()
        ins = e.compile("巡查 巡检台\n采集 十城 \n\n入库 成果")
        self.assertEqual([i["seq"] for i in ins], [1, 2, 3])          # 空行不占序号
        self.assertEqual([i["verb"] for i in ins], ["巡查", "采集", "入库"])
        self.assertEqual([i["object"] for i in ins], ["巡检台", "十城", "成果"])

    def test_unknown_verb_rejected(self):
        e = Edict()
        with self.assertRaises(ValueError) as cm:
            e.compile("胡来 天下")
        self.assertIn("未知动词", str(cm.exception))

    def test_empty_object_rejected(self):
        e = Edict()
        with self.assertRaises(ValueError) as cm:
            e.compile("体检")
        self.assertIn("对象为空", str(cm.exception))

    def test_render_roundtrip(self):
        e = Edict()
        text = "生长 金匮\n上报 体系总控 when 2026-11-02T08:00\n体检 全域"
        ins = e.compile(text)
        self.assertEqual(e.render(ins), text)                          # 往返一致
        # 反向：先编译再渲染再编译，仍得同一指令序列
        again = e.compile(e.render(ins))
        self.assertEqual(again, ins)

    def test_when_validated(self):
        e = Edict()
        ok = e.compile("上报 成果 when 2026-11-02")
        self.assertEqual(ok[0]["when"], "2026-11-02")
        with self.assertRaises(ValueError):
            e.compile("上报 成果 when 十一月初二")

    def test_describe_stage(self):
        d = Edict().describe()
        self.assertEqual(d["name"], "tianzhuan")
        self.assertEqual(d["stage"], "m1")

if __name__ == "__main__":
    unittest.main()
