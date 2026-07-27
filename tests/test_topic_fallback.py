import unittest

from ai_service import AIService


class TopicFallbackTests(unittest.TestCase):
    def test_build_topic_analysis_fallback_returns_content(self):
        service = AIService()
        result = service._build_topic_analysis_fallback("Begrüßung & Sich Vorstellen", "A1")

        self.assertEqual(result["topic"], "Begrüßung & Sich Vorstellen")
        self.assertEqual(result["level"], "A1")
        self.assertIn("Selamlaşma", result["summary_tr"])
        self.assertGreaterEqual(len(result["key_grammar_rules"]), 3)
        self.assertGreaterEqual(len(result["examples"]), 3)
        self.assertGreaterEqual(len(result["mini_quiz"]), 5)

    def test_build_topic_analysis_fallback_uses_topic_keywords(self):
        service = AIService()
        result = service._build_topic_analysis_fallback("Perfekt mit sein", "A2")

        self.assertIn("Perfekt", result["summary_tr"])
        self.assertTrue(any("sein" in rule.lower() for rule in result["key_grammar_rules"]))


if __name__ == "__main__":
    unittest.main()
