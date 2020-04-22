# hotel-reviews-text-classification
Implementation of a Naive Bayes classifier to identify hotel reviews as either truthful or deceptive, and either positive or negative

## Data 

A set of training and development data containing the following files:

 - A top-level directory with two sub-directories, one for positive reviews and another for negative reviews.
 - Each of the subdirectories contains two sub-directories, one with truthful reviews and one with deceptive reviews.
 - Each of these subdirectories contains four subdirectories, called “folds”.
 - Each of the folds contains 80 text files with English text (one review per file).

## Programs
nblearn.py will learn a naive Bayes model from the training data, and nbclassify.py will use the model to classify new data.

The file can be executed the following way: ```python nblearn.py /path/to/training_data ```
The argument is the directory of the training data; the program will learn a naive Bayes model, and write the model parameters to a file called nbmodel.txt. 

The classification program will be executed the following way: ``` python nbclassify.py /path/to/test_data ```

The argument is the directory of the test data; the program will read the parameters of a naive Bayes model from the file nbmodel.txt, classify each file in the test data, and write the results to a text file called nboutput.txt in the following format: 
```label_a label_b path1```
    
In the above format, label_a is either “truthful” or “deceptive”, label_b is either “positive” or “negative”, and pathn is the path of the text file being classified.

## Results

|  Attribute | Precision  | Recall  |  F1   |
|------------|------------|---------|-------|
| deceptive  |   0.73     |  0.91   | 0.81  |
| truthful   |   0.88     |  0.67   | 0.76  |
| negative   |   0.99     |  0.79   | 0.88  |
| positive   |   0.83     |  0.99   | 0.90  |

Mean F1 Score :  0.8386
