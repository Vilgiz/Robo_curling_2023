import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.model_selection import train_test_split, GridSearchCV
import joblib
import cv2
import os

class Detecter():
    def __init__(self, new = False):
        self.poly = PolynomialFeatures(degree=2)
        self.dir = os.path.dirname(__file__)
        if new:
            self.model = LogisticRegression(random_state=0, multi_class='ovr',max_iter = 5000)
            self.scaler = StandardScaler()
        else:
            self.__load_configs()

    def __load_configs(self):
        self.model = joblib.load('model.pkl')
        self.scaler = joblib.load('scaler.pkl')

    def save_configs(self):
        joblib.dump(self.model, 'model.pkl')
        joblib.dump(self.scaler, 'scaler.pkl')

    def add_noise(self, noise_force):
        augmented_data = []
        for point in self.data:
            augmented_point = []
            for feature in point:
                noise = np.random.normal(0, noise_force)
                augmented_feature = feature + noise
                augmented_point.append(augmented_feature)
            augmented_data.append(augmented_point)
        return augmented_data
    
    def __prepare_data(self, Classes):
        Class0 = Classes[0]
        Class1 = Classes[1]
        Class2 = Classes[2]
        #Class = [[a,b,c],[d,e,f],...]
        raw_x = Class0 + Class1 + Class2
        raw_y = [0] * len(Class0) + [1] * len(Class1) + [-1] * len(Class2)

        xpoly = self.poly.fit_transform(raw_x)[:,1:]
        x_train_raw, x_test_raw, y_train, y_test = train_test_split(xpoly , raw_y, test_size=0.3, random_state=0)
        self.scaler.fit(x_train_raw)
        x_train = self.scaler.transform(x_train_raw)
        x_test = self.scaler.transform(x_test_raw)

        return(x_train, y_train, x_test, y_test)

    def _train_model(self, Classes):
        #Classes = [Class0, Class1, Class2]
        x_train, y_train, x_test, y_test = self.__prepare_data(Classes)
        param_grid = [ { 'C': np.logspace(-3, 3, num=10) } ]
        lr_search = LogisticRegression(random_state=0, multi_class='ovr', max_iter = 5000)
        grid = GridSearchCV(lr_search, param_grid)
        grid.fit(x_train, y_train)

        self.model = grid.best_estimator_
        self.model.fit(x_train, y_train)

        err_train = np.mean(y_train != self.model.predict(x_train)) 
        err_test = np.mean(y_test != self.model.predict(x_test)) 
        print("\n err_train = ", err_train, "\n err_test = ", err_test) 

    def force_training(self, path, retrain = False):
        
        self.__take_manual_data(path)
        Cap = cv2.VideoCapture(path)
        Classes = []

        _, frame = Cap.read()
        while _:
            cv2.imshow('Video', frame)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            for j in self.data_monitor:
                buf = []
                for i in j: buf.append(hsv[i[1], i[0]].tolist())
                Classes.append(buf)
            _, frame = Cap.read()
        
        if retrain: self.model.set_params(warm_start = True)
        else: self.model.set_params(warm_start = False)
        self._train_model (Classes)
    
    def __take_manual_data(self, path):
        self.data_monitor = []
        buf = []
        def mouse_callback(event, x, y,flags,params):
            if event == cv2.EVENT_LBUTTONDOWN:
                buf.append([x,y])

        cap = cv2.VideoCapture(path)
        cv2.namedWindow('Video')
        cv2.setMouseCallback('Video', mouse_callback)
        _, frame = cap.read()
        cv2.imshow('Video', frame)
        while True:
            key = cv2.waitKey(1)& 0xFF
            if  key == ord('n'):
                self.data_monitor.append(buf)
                buf = []
                print('next')
                
            if key == ord('q'):
                print(self.data_monitor)
                break

        cap.release()
        cv2.destroyAllWindows()


    def designate (self, data):
        data = self.poly.fit_transform(data)[:,1:]
        data = self.scaler.transform(data)
        results = self.model.predict(data)
        return (results)
    


if __name__ == '__main__':
    #test = Detecter(new = True)
    test = Detecter()
    path = os.path.join(test.dir,'datasets','train.mp4')
    print (path)
    #test.force_training(path)
    #test.force_training(path, retrain = True)
    #test.save_configs()
    data = np.array([1,190,210]).reshape(1, -1)
    res = test.designate(data)
    print (res)
