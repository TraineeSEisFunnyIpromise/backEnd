
#-------------------------import library Above-----------------------------
#-------------------------set up mongoDB for testing Above-----------------------------


# classifier = transformers.pipeline("zero-shot-classification", model="facebook/bart-large-mnli")  
# #sample text and label


# def compare_prod(criteria_lists, inputa):
# 	prediction = classifier(inputa, criteria_lists)
# 	return prediction

# def compare_test(criteria_lists, inputa):
# 	prediction = classifier(inputa, criteria_lists)  

# 	print(prediction['sequence']) 
# 	print(prediction['labels']) 
# 	print(prediction['scores'])

from transformers import pipeline

# Initialize the zero-shot classification pipeline
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Function to classify and sum scores for each label dynamically
def classify_and_sum_scores(input_texts, input_labels):
    total_scores = {label: 0.0 for label in input_labels}
    
    for text in input_texts:
        result = classifier(text, input_labels)
        for label, score in zip(result['labels'], result['scores']):
            total_scores[label] += score
    return total_scores

def calculate_the_zeroshot(input_texts, dynamic_labels):
    print("Before function:")

    filtered_input_texts = []
    for item in input_texts:
        if isinstance(item, dict) and 'Review Texts' in item: 
            review_text = item['Review Texts'] 
            if review_text != None and review_text != 'None':
                filtered_input_texts.append(review_text) 

    print("Filtered input texts:")
    print(filtered_input_texts)
    print("Before check")
    if not filtered_input_texts:
        return []  # Return an empty list if no valid input texts remain

    # Calculate the sum of scores for the dynamic labels
    total_scores = classify_and_sum_scores(filtered_input_texts, dynamic_labels) 
    print("calculate")
    for label in total_scores:
        total_scores[label] = total_scores[label] / len(filtered_input_texts)
        print(f"Total score for {label}: {total_scores[label]}")

    # Create a list of data rows
    data = [{'Label': label, 'Score': score} for label, score in total_scores.items()]
    print("exit function")
    return data


# def calculate_the_zeroshot_test():
#     # Calculate the sum of scores for the dynamic labels
#     text = "I enjoy playing cricket, specializing as a left-arm leg spinner while showcasing my skills as a right-handed one-down batsman." 
#     labels = ['Politics', 'Automobile', 'Sports', 'Business', 'World']  
#     total_scores = classify_and_sum_scores(text, labels)
#     for label in total_scores:
#         total_scores[label] = total_scores[label] / len(text)
        


#     # Create a list of data rows
#     data= [{'Label': label, 'Score': score} for label, score in total_scores.items()]
#     print(data)
#     return data
    