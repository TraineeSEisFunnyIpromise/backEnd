import unittest
from Reqandscrape.requestsender.chatgptreqsender import extract_criteria as convert_input

class TestChangeData(unittest.TestCase):


    def test_success_convert_input(self):
        criteria = """Capacity: Do you usually toast for one or two people? Standard toasters have 2 slices, but wider models can handle 4.
Slot size: Consider what types of bread you toast. If you like bagels or thick Texas toast, wider slots are a must. Long slots are handy for long slices of bread.
Browning controls: How precise do you want your toast? Some toasters have a simple dial, while others offer many shade settings for perfectly customized browning.
Features: Do you want a defrost function for frozen bread? A reheat setting for keeping toast warm? Bagel setting that toasts the inside but barely touches the outside? Consider which features would be most useful to you.
Ease of cleaning: Look for a toaster with a removable crumb tray for easy cleaning.
Budget: Toasters range in price from basic models to high-end ones with lots of features. Decide how much you're comfortable spending.
Style: While not the most important factor, some toasters come in a variety of styles to match your kitchen décor."""
        result = convert_input(criteria)
        self.assertIsNotNone(result)

    
    def test_unsuccess_convert_input(self):
        result = convert_input(None)
        self.assertIsNone(result)
    
if __name__ == '__main__':
    unittest.main()
