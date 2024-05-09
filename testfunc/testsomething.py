import re

sentence = """Capacity: Do you usually toast for one or two people? Standard toasters have 2 slices, but wider models can handle 4.
Slot size: Consider what types of bread you toast. If you like bagels or thick Texas toast, wider slots are a must. Long slots are handy for long slices of bread.
Browning controls: How precise do you want your toast? Some toasters have a simple dial, while others offer many shade settings for perfectly customized browning.
Features: Do you want a defrost function for frozen bread? A reheat setting for keeping toast warm? Bagel setting that toasts the inside but barely touches the outside? Consider which features would be most useful to you.
Ease of cleaning: Look for a toaster with a removable crumb tray for easy cleaning.
Budget: Toasters range in price from basic models to high-end ones with lots of features. Decide how much you're comfortable spending.
Style: While not the most important factor, some toasters come in a variety of styles to match your kitchen décor."""

def select_headline(text):
  match = re.search(r"(.*):\s+(\w+)", text)  # Matches text followed by ":" and a word
  if match:
    return match.group(1) + ":"  # Captures group 1 (text before ":") and adds ":"
  else:
    return None  # Return None if no match


def segment_text(text):
  """
  Segments the text at "." (periods).
  """
  segments = re.split(r"\.", text)  # Split at "."
  return segments

def segment_semi(text):
  text = segment_text(sentence)
  storea = []
  for i in range(len(text)):
    storea.append(select_headline(text[i]))
  print(storea)
  print("------")

headline = sentence
something = segment_text(headline)
somethinga = segment_semi(something)
print("--------------------TEXT--------------------")
print(something)
print("-------------------SEMI---------------------")
print(segment_semi(something))
print("-------------------CLEAN---------------------")
print("------------------END----------------------")