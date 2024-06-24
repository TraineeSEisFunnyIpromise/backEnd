import transformers  

classifier = transformers.pipeline("zero-shot-classification", model="facebook/bart-large-mnli")  

text = "I enjoy playing cricket, specializing as a left-arm leg spinner while showcasing my skills as a right-handed one-down batsman." 
labels = ['Politics', 'Automobile', 'Sports', 'Business', 'World']  

prediction = classifier(text, labels)  

print(prediction['sequence']) 
print(prediction['labels']) 
print(prediction['scores'])