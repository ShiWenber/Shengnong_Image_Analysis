# C++ ��ͨ�����(Connected Component Analysis)



```C++
// hello_opencv.cpp : ���ļ����� "main" ����������ִ�н��ڴ˴���ʼ��������
//
#include <opencv2\opencv.hpp>
#include <iostream>
#include <fstream>

using namespace std;
using namespace cv;

int main()
{
    /*
    Mat src = imread("C:\\Users\\shiwenbo\\OneDrive\\images\\proc.jpg", IMREAD_GRAYSCALE);
	namedWindow("���봰��",WINDOW_FREERATIO);
	imshow("���봰��", src);
	waitKey(100000);
	destroyAllWindows();
    */
    // ͼƬ·��
	string imagePath = "C:\\Users\\shiwenbo\\OneDrive\\images\\4-21\\2022-04-21T17_00_26+08_00\\proc.jpg";


    Mat src = imread(imagePath, IMREAD_GRAYSCALE);

	imshow("���봰��", src);
	waitKey(0);
	destroyAllWindows();



    // ��ֵ��ͼ��ָ�

    system("color F0");  //�������������ɫ
    //��ͼ����о���任
    Mat img = imread(imagePath);
    if (img.empty())
    {
        cout << "��ȷ��ͼ���ļ������Ƿ���ȷ" << endl;
        return -1;
    }
    imshow(imagePath, img);
    Mat leaves, leavesBW;

    //��ͼ��ת�ɶ�ֵͼ������ͳ����ͨ��
    cvtColor(img, leaves, COLOR_BGR2GRAY);
    threshold(leaves,leavesBW, 50, 255, THRESH_BINARY);

    //���������ɫ���������ֲ�ͬ��ͨ��
    RNG rng(10086);
    Mat out, stats, centroids;
    //ͳ��ͼ������ͨ��ĸ���
    int number = connectedComponentsWithStats(leavesBW, out, stats, centroids, 8, CV_16U);
    vector<Vec3b> colors;
    for (int i = 0; i < number; i++)
    {
        //ʹ�þ��ȷֲ��������ȷ����ɫ
        Vec3b vec3 = Vec3b(rng.uniform(0, 256), rng.uniform(0, 256), rng.uniform(0, 256));
        colors.push_back(vec3);
    }

    // �����ļ�
    // 
    //�Բ�ͬ��ɫ��ǳ���ͬ����ͨ��
    Mat result = Mat::zeros(leaves.size(), img.type());
    int w = result.cols;
    int h = result.rows;
    for (int i = 1; i < number; i++)
    {
        // ����λ��
        int center_x = centroids.at<double>(i, 0);
        int center_y = centroids.at<double>(i, 1);
        //���α߿�
        int x = stats.at<int>(i, CC_STAT_LEFT);
        int y = stats.at<int>(i, CC_STAT_TOP);
        int w = stats.at<int>(i, CC_STAT_WIDTH);
        int h = stats.at<int>(i, CC_STAT_HEIGHT);
        int area = stats.at<int>(i, CC_STAT_AREA);

        // ����λ�û���
        circle(img, Point(center_x, center_y), 2, Scalar(0, 255, 0), 2, 8, 0);
        // ��Ӿ���
        Rect rect(x, y, w, h);
        rectangle(img, rect, colors[i], 1, 8, 0);
        putText(img, format("%d", i), Point(center_x, center_y),
            FONT_HERSHEY_SIMPLEX, 0.5, Scalar(0, 0, 255), 1);
        cout << "number: " << i << ",area: " << area << endl;


    }
    //��ʾ���
    imshow("��Ǻ��ͼ��", img);

    waitKey(0);
    return 0;







}

// ���г���: Ctrl + F5 ����� >����ʼִ��(������)���˵�
// ���Գ���: F5 ����� >����ʼ���ԡ��˵�

// ����ʹ�ü���: 
//   1. ʹ�ý��������Դ�������������/�����ļ�
//   2. ʹ���Ŷ���Դ�������������ӵ�Դ�������
//   3. ʹ��������ڲ鿴���������������Ϣ
//   4. ʹ�ô����б��ڲ鿴����
//   5. ת������Ŀ��>���������Դ����µĴ����ļ�����ת������Ŀ��>�����������Խ����д����ļ���ӵ���Ŀ
//   6. ��������Ҫ�ٴδ򿪴���Ŀ����ת�����ļ���>���򿪡�>����Ŀ����ѡ�� .sln �ļ�

```

The next part is the code which is complete and there is redundant code for visualizing and debugging.

```C++
// hello_opencv.cpp : ���ļ����� "main" ����������ִ�н��ڴ˴���ʼ��������
//
#include <opencv2\opencv.hpp>
#include <iostream>
#include <fstream>

using namespace std;
using namespace cv;

vector<Vec3b> colors;
Mat displayImage(Mat, Mat);
int imageId = 1;
void statsWrite(string, Mat);


Mat removeRow(Mat src, Mat& dst, int row) {
    if (src.rows == 1) {
        dst = src;
        return src;
    }
    Mat res1;
    Mat res2;
    Mat input = src.clone();
    input(Range(0, row), Range(0, input.cols)).copyTo(res1);
    // ���res2����Ϊ0���ϲ��ͻᱨ��
    if (row + 1 < input.rows) {
        input(Range(row + 1, input.rows), Range(0, input.cols)).copyTo(res2);
        // �ϲ�����
        vconcat(res1, res2, res1);
        dst = res1.clone();
    } else {
        dst = res1.clone();
        
    }
    return res1;

}



// �ϲ���ͨ���
Mat combineStats(Mat src, Mat& dst, Mat img, float threshold = 0) {
    Mat input = src.clone();
    for (int i = 1; i < input.rows; i++) {
        int x1 = input.at<int>(i, CC_STAT_LEFT);
        int y1 = input.at<int>(i, CC_STAT_TOP);
        int w1 = input.at<int>(i, CC_STAT_WIDTH);
        int h1 = input.at<int>(i, CC_STAT_HEIGHT);
        int area1 = input.at<int>(i, CC_STAT_AREA);

        for (int j = i + 1; j < input.rows; j++) {
            int x2 = input.at<int>(j, CC_STAT_LEFT);
            int y2 = input.at<int>(j, CC_STAT_TOP);
            int w2 = input.at<int>(j, CC_STAT_WIDTH);
            int h2 = input.at<int>(j, CC_STAT_HEIGHT);
            int area2 = input.at<int>(j, CC_STAT_AREA);
            // �ж�1 �� 2�������Ƿ��ص� ����ʽԭ����leetcode�����Ŀ��https://blog.csdn.net/qq_43539599/article/details/104952828
            // int notOverlapped = (x1 + w1 < x2 || x2 + w2 < x1 || y1 + h1 < y2 || y2 + h2 < y1);
            int overlapped = (x1 < x2 + w2 && x2 < x1 + w1 && y1 < y2 + h2 && y2 < y1 + h1);

            if (overlapped == 0) {
                continue;
            }

            // ȷ���ص����߽�
            int left = max(x1, x2);
            int top = max(y1, y2);
            int right = min(x1 + w1, x2 + w2);
            int bottom = min(y1 + h1, y2 + h2);


            // �����ص��������
            int overlap = (right - left) * (bottom - top);

            // ����ص��������������ֵ����ϲ�����
            if (overlap > threshold) {
                // ȷ���ϲ������ x, y, w, h, area
                int x = min(x1, x2);
                int y = min(y1, y2);
                int w = max(x1 + w1, x2 + w2) - x;
                int h = max(y1 + h1, y2 + h2) - y;
                int area = area1 + area2;
                input.at<int>(i, CC_STAT_LEFT) = x;
                input.at<int>(i, CC_STAT_TOP) = y;
                input.at<int>(i, CC_STAT_WIDTH) = w;
                input.at<int>(i, CC_STAT_HEIGHT) = h;
                input.at<int>(i, CC_STAT_AREA) = area;
                // ɾ�����ϲ���x2����
                if (input.rows == 2) {
                    dst = input.clone();
                    return input;
                }
                removeRow(input, input, j);
                // ��������1
                x1 = x;
                y1 = y;
                w1 = w;
                h1 = h;
                area1 = area;

                j--; // ��λ
                // displayImage(img, input); // ����ʹ��
            }


        }


    }
    dst = input.clone();
    return input;
}

Mat sortrows(Mat src, Mat& dst, int sort_col) {
    Mat input = src.clone();
    // ��ð������������mat
    for (int i = 0; i < input.rows; i++) {
        for (int j = 0; j < input.rows - i - 1; j++) {
            if (input.at<int>(j, sort_col) < input.at<int>(j + 1, sort_col)) {
                Mat temp = input.row(j + 1).clone();
                input.row(j).copyTo(input.row(j + 1));
                temp.row(0).copyTo(input.row(j));
            }
        }
    }
    dst = input.clone();
    return input;

}

void statsWrite(string filepath, Mat stats) {
    // �½�һ���ļ�����¼����
	ofstream outfile;
	outfile.open(filepath, ios::out); // �������߸����ļ�
    // ��ͷ
    outfile << "id" << ", " << "area" << "," << "x" << ", " << "y" << ", " << "w" << ", " << "h" << endl;
    for (int i = 1; i < stats.rows; i++) {
        int x = stats.at<int>(i, CC_STAT_LEFT);
        int y = stats.at<int>(i, CC_STAT_TOP);
        int w = stats.at<int>(i, CC_STAT_WIDTH);
        int h = stats.at<int>(i, CC_STAT_HEIGHT);
        int area = stats.at<int>(i, CC_STAT_AREA);

        outfile << i << ", " << area << "," << x << ", " << y << ", " << w << ", " << h << endl;

    }
    outfile.close();
}

Mat displayImage(Mat img, Mat stats) {
    Mat temp_img = img.clone();
    int number = stats.rows;
    sortrows(stats, stats, CC_STAT_AREA);
    cout << stats << endl;

    // �����ͨ����ȫ��ͼ���������������stats��һ��Ҫȥ��
    for (int i = 1; i < number; i++)
    {
        // ����λ��
        int center_x = stats.at<int>(i, CC_STAT_LEFT) + stats.at<int>(i, CC_STAT_WIDTH) / 2;
		int center_y = stats.at<int>(i, CC_STAT_TOP) + stats.at<int>(i, CC_STAT_HEIGHT) / 2;
            //���α߿�
        int x = stats.at<int>(i, CC_STAT_LEFT);
        int y = stats.at<int>(i, CC_STAT_TOP);
        int w = stats.at<int>(i, CC_STAT_WIDTH);
        int h = stats.at<int>(i, CC_STAT_HEIGHT);
        int area = stats.at<int>(i, CC_STAT_AREA);

        // ����֮ǰ�ȱ�����������Ƿ���ڿ��Ժϲ�������

        // ����λ�û���
        //circle(temp_img, Point(center_x, center_y), 2, Scalar(0, 255, 0), 2, 8, 0);
        circle(temp_img, Point(center_x, center_y), 2, colors[i], 2, 8, 0);
        // ��Ӿ���
        Rect rect(x, y, w, h);
        rectangle(temp_img, rect, colors[i], 1, 8, 0);
        //putText(temp_img, format("%d", i + 1), Point(center_x, center_y),
        //    FONT_HERSHEY_SIMPLEX, 0.5, Scalar(0, 0, 255), 1);
        putText(temp_img, format("%d", i), Point(center_x, center_y),
            FONT_HERSHEY_SIMPLEX, 0.5, colors[i], 1);

        cout << "number: " << i << ",area: " << area <<
            ",x: " << x <<
            ",y: " << y <<
            ",w: " << w <<
            ",h: " << h << endl;


    }
    //��ʾ���
    
    imshow(to_string(imageId++), temp_img);

    waitKey(0);
    return temp_img;

}


int main(int argc, char **argv)
{
    /*
    Mat src = imread("C:\\Users\\shiwenbo\\OneDrive\\images\\proc.jpg", IMREAD_GRAYSCALE);
	namedWindow("���봰��",WINDOW_FREERATIO);
	imshow("���봰��", src);
	waitKey(100000);
	destroyAllWindows();
    */
    // ͼƬ·��
	// string imagePath = "C:\\Users\\shiwenbo\\OneDrive\\images\\2022-04-21\\2022-04-21T17_00_26+08_00\\";
    string imagePath;
    imagePath = argv[1];
	
    string imageFileName = "proc.jpg";





    // ��ֵ��ͼ��ָ�

    system("color F0");  //�������������ɫ
    //��ͼ����о���任
    Mat img = imread(imagePath + imageFileName);
    Mat originImage = img.clone();
    if (img.empty())
    {
        cout << "��ȷ��ͼ���ļ������Ƿ���ȷ" << endl;
        return -1;
    }
    imshow(imagePath + imageFileName, img);

    Mat leaves, leavesBW;

    //��ͼ��ת�ɶ�ֵͼ������ͳ����ͨ��
    cvtColor(img, leaves, COLOR_BGR2GRAY);
    threshold(leaves,leavesBW, 50, 255, THRESH_BINARY);

    //���������ɫ���������ֲ�ͬ��ͨ��
    RNG rng(10086);
    Mat out, stats, centroids;
    //ͳ��ͼ������ͨ��ĸ���
    int number = connectedComponentsWithStats(leavesBW, out, stats, centroids, 8, CV_16U);
    for (int i = 0; i < number; i++)
    {
        //ʹ�þ��ȷֲ��������ȷ����ɫ
        Vec3b vec3 = Vec3b(rng.uniform(0, 256), rng.uniform(0, 256), rng.uniform(0, 256));
        colors.push_back(vec3);
    }

    // �����ļ�
    // 
    //�Բ�ͬ��ɫ��ǳ���ͬ����ͨ��
    //Mat result = Mat::zeros(leaves.size(), img.type());
	
    //int w = result.cols;
    //int h = result.rows;
    sortrows(stats, stats, CC_STAT_AREA);
    cout << stats << endl;
    
    // �����ͨ����ȫ��ͼ���������������stats��һ��Ҫȥ��
    for (int i = 1; i < number; i++)
    {
        // ����λ��
        int center_x = centroids.at<double>(i, 0);
        int center_y = centroids.at<double>(i, 1);
        //���α߿�
        int x = stats.at<int>(i, CC_STAT_LEFT);
        int y = stats.at<int>(i, CC_STAT_TOP);
        int w = stats.at<int>(i, CC_STAT_WIDTH);
        int h = stats.at<int>(i, CC_STAT_HEIGHT);
        int area = stats.at<int>(i, CC_STAT_AREA);

		
		// ����֮ǰ�ȱ�����������Ƿ���ڿ��Ժϲ�������

        // ����λ�û���
        //circle(img, Point(center_x, center_y), 2, Scalar(0, 255, 0), 2, 8, 0);
        circle(img, Point(center_x, center_y), 2, colors[i], 2, 8, 0);
        // ��Ӿ���
        Rect rect(x, y, w, h);
        rectangle(img, rect, colors[i], 1, 8, 0);
        //putText(img, format("%d", i + 1), Point(center_x, center_y),
        //    FONT_HERSHEY_SIMPLEX, 0.5, Scalar(0, 0, 255), 1);
        putText(img, format("%d", i), Point(center_x, center_y),
            FONT_HERSHEY_SIMPLEX, 0.5,colors[i], 1);


        cout << "number: " << i + 1 << ",area: " << area << endl;


		
        // �½�һ���ļ�����¼����
		ofstream outfile;
		outfile.open(imagePath + "proc.csv", ios::app); // ios::app���û���ļ������ɿ��ļ�����������ļ��������ļ�β׷��

	    outfile << "number: " << i << ",area: " << area  << 
            ",x: " << x <<
            ",y: " << y <<
			",w: " << w <<
			",h: " << h << endl;
        outfile.close();
        

    }
    //��ʾ���
    imshow("��Ǻ��ͼ��", img);

    imwrite(imagePath + "proc2.jpg", img);

    waitKey(0);

    Mat temp;
    combineStats(stats, temp,originImage, 0);
    sortrows(temp, temp, CC_STAT_AREA);
    Mat resImg = displayImage(originImage, temp);
    // ������ͼ
    imwrite(imagePath + "proc3.jpg", resImg);
    // ������stats��ͨ���
    statsWrite(imagePath + "combined_stats.csv", temp);


	

    return 0;
}

// ���г���: Ctrl + F5 ����� >����ʼִ��(������)���˵�
// ���Գ���: F5 ����� >����ʼ���ԡ��˵�

// ����ʹ�ü���: 
//   1. ʹ�ý��������Դ�������������/�����ļ�
//   2. ʹ���Ŷ���Դ�������������ӵ�Դ�������
//   3. ʹ��������ڲ鿴���������������Ϣ
//   4. ʹ�ô����б��ڲ鿴����
//   5. ת������Ŀ��>���������Դ����µĴ����ļ�����ת������Ŀ��>�����������Խ����д����ļ���ӵ���Ŀ
//   6. ��������Ҫ�ٴδ򿪴���Ŀ����ת�����ļ���>���򿪡�>����Ŀ����ѡ�� .sln �ļ�

```

2022.5.24 stable code

```C++
// hello_opencv.cpp : ���ļ����� "main" ����������ִ�н��ڴ˴���ʼ��������
//
#include <opencv2\opencv.hpp>
#include <iostream>
#include <fstream>

using namespace std;
using namespace cv;

vector<Vec3b> colors;
Mat displayImage(Mat, Mat, bool, int);
int imageId = 1;
void statsWrite(string, Mat);


Mat removeRow(Mat src, Mat& dst, int row) {
    if (src.rows == 1) {
        dst = src;
        return src;
    }
    Mat res1;
    Mat res2;
    Mat input = src.clone();
    input(Range(0, row), Range(0, input.cols)).copyTo(res1);
    // ���res2����Ϊ0���ϲ��ͻᱨ��
    if (row + 1 < input.rows) {
        input(Range(row + 1, input.rows), Range(0, input.cols)).copyTo(res2);
        // �ϲ�����
        vconcat(res1, res2, res1);
        dst = res1.clone();
    } else {
        dst = res1.clone();
        
    }
    return res1;

}



// �ϲ���ͨ���
Mat combineStats(Mat src, Mat& dst, Mat img, float threshold = 0) {
    Mat input = src.clone();
    for (int i = 1; i < input.rows; i++) {
        int x1 = input.at<int>(i, CC_STAT_LEFT);
        int y1 = input.at<int>(i, CC_STAT_TOP);
        int w1 = input.at<int>(i, CC_STAT_WIDTH);
        int h1 = input.at<int>(i, CC_STAT_HEIGHT);
        int area1 = input.at<int>(i, CC_STAT_AREA);

        for (int j = i + 1; j < input.rows; j++) {
            int x2 = input.at<int>(j, CC_STAT_LEFT);
            int y2 = input.at<int>(j, CC_STAT_TOP);
            int w2 = input.at<int>(j, CC_STAT_WIDTH);
            int h2 = input.at<int>(j, CC_STAT_HEIGHT);
            int area2 = input.at<int>(j, CC_STAT_AREA);
            // �ж�1 �� 2�������Ƿ��ص� ����ʽԭ����leetcode�����Ŀ��https://blog.csdn.net/qq_43539599/article/details/104952828
            // int notOverlapped = (x1 + w1 < x2 || x2 + w2 < x1 || y1 + h1 < y2 || y2 + h2 < y1);
            int overlapped = (x1 < x2 + w2 && x2 < x1 + w1 && y1 < y2 + h2 && y2 < y1 + h1);

            if (overlapped == 0) {
                continue;
            }

            // ȷ���ص����߽�
            int left = max(x1, x2);
            int top = max(y1, y2);
            int right = min(x1 + w1, x2 + w2);
            int bottom = min(y1 + h1, y2 + h2);


            // �����ص��������
            int overlap = (right - left) * (bottom - top);

            // ����ص��������������ֵ����ϲ�����
            if (overlap > threshold) {
                // ȷ���ϲ������ x, y, w, h, area
                int x = min(x1, x2);
                int y = min(y1, y2);
                int w = max(x1 + w1, x2 + w2) - x;
                int h = max(y1 + h1, y2 + h2) - y;
                int area = area1 + area2;
                input.at<int>(i, CC_STAT_LEFT) = x;
                input.at<int>(i, CC_STAT_TOP) = y;
                input.at<int>(i, CC_STAT_WIDTH) = w;
                input.at<int>(i, CC_STAT_HEIGHT) = h;
                input.at<int>(i, CC_STAT_AREA) = area;
                // ɾ�����ϲ���x2����
                if (input.rows == 2) {
                    dst = input.clone();
                    return input;
                }
                removeRow(input, input, j);
                // ��������1
                x1 = x;
                y1 = y;
                w1 = w;
                h1 = h;
                area1 = area;

                j--; // ��λ
            }

            displayImage(img, input,true, 0);

        }


    }
    dst = input.clone();
    return input;
}

Mat sortrows(Mat src, Mat& dst, int sort_col) {
    Mat input = src.clone();
    // ��ð������������mat
    for (int i = 0; i < input.rows; i++) {
        for (int j = 0; j < input.rows - i - 1; j++) {
            if (input.at<int>(j, sort_col) < input.at<int>(j + 1, sort_col)) {
                Mat temp = input.row(j + 1).clone();
                input.row(j).copyTo(input.row(j + 1));
                temp.row(0).copyTo(input.row(j));
            }
        }
    }
    dst = input.clone();
    return input;

}

void statsWrite(string filepath, Mat stats) {
    // �½�һ���ļ�����¼����
	ofstream outfile;
	outfile.open(filepath, ios::out); // �������߸����ļ�
    // ��ͷ
    outfile << "id" << ", " << "area" << "," << "x" << ", " << "y" << ", " << "w" << ", " << "h" << endl;
    for (int i = 1; i < stats.rows; i++) {
        int x = stats.at<int>(i, CC_STAT_LEFT);
        int y = stats.at<int>(i, CC_STAT_TOP);
        int w = stats.at<int>(i, CC_STAT_WIDTH);
        int h = stats.at<int>(i, CC_STAT_HEIGHT);
        int area = stats.at<int>(i, CC_STAT_AREA);

        outfile << i << ", " << area << "," << x << ", " << y << ", " << w << ", " << h << endl;

    }
    outfile.close();
}

// �����ͨ����Ϣ�������ݲ���չʾͼƬ
Mat displayImage(Mat img, Mat stats, bool is_imshow = false, int showtime = 0) {
    Mat temp_img = img.clone();
    int number = stats.rows;
    sortrows(stats, stats, CC_STAT_AREA);

    // �����ͨ����ȫ��ͼ���������������stats��һ��Ҫȥ��
    for (int i = 1; i < number; i++)
    {
        // ����λ��
        int center_x = stats.at<int>(i, CC_STAT_LEFT) + stats.at<int>(i, CC_STAT_WIDTH) / 2;
		int center_y = stats.at<int>(i, CC_STAT_TOP) + stats.at<int>(i, CC_STAT_HEIGHT) / 2;
            //���α߿�
        int x = stats.at<int>(i, CC_STAT_LEFT);
        int y = stats.at<int>(i, CC_STAT_TOP);
        int w = stats.at<int>(i, CC_STAT_WIDTH);
        int h = stats.at<int>(i, CC_STAT_HEIGHT);
        int area = stats.at<int>(i, CC_STAT_AREA);

        // ����֮ǰ�ȱ�����������Ƿ���ڿ��Ժϲ�������

        // ����λ�û���
        //circle(temp_img, Point(center_x, center_y), 2, Scalar(0, 255, 0), 2, 8, 0);
        circle(temp_img, Point(center_x, center_y), 2, colors[i], 2, 8, 0);
        // ��Ӿ���
        Rect rect(x, y, w, h);
        rectangle(temp_img, rect, colors[i], 1, 8, 0);
        //putText(temp_img, format("%d", i + 1), Point(center_x, center_y),
        //    FONT_HERSHEY_SIMPLEX, 0.5, Scalar(0, 0, 255), 1);
        putText(temp_img, format("%d", i), Point(center_x, center_y),
            FONT_HERSHEY_SIMPLEX, 0.5, colors[i], 1);
    }
    //��ʾ���
    
    if (is_imshow) {
		imshow("result-" + to_string(imageId++), temp_img);
		waitKey(showtime);
	}

    return temp_img;

}

// ʹ��˵���� ��ִ���ļ���Ĳ���Ӧ���ǲ�����/��
int main(int argc, char **argv)
{
    string imagePath;
    imagePath = argv[1];
    imagePath += "\\";
	
    string imageFileName = "proc.jpg";





    // ��ֵ��ͼ��ָ�

    system("color F0");  //�������������ɫ
    //��ͼ����о���任
    Mat img = imread(imagePath + imageFileName);
    Mat originImage = img.clone();
    if (img.empty())
    {
        cout << "��ȷ��ͼ���ļ������Ƿ���ȷ" << endl;
        return -1;
    }

    Mat leaves, leavesBW;

    //��ͼ��ת�ɶ�ֵͼ������ͳ����ͨ��
    cvtColor(img, leaves, COLOR_BGR2GRAY);
    threshold(leaves,leavesBW, 50, 255, THRESH_BINARY);

    //���������ɫ���������ֲ�ͬ��ͨ��
    RNG rng(10086);
    Mat out, stats, centroids;
    //ͳ��ͼ������ͨ��ĸ���
    int number = connectedComponentsWithStats(leavesBW, out, stats, centroids, 8, CV_16U);
    for (int i = 0; i < number; i++)
    {
        //ʹ�þ��ȷֲ��������ȷ����ɫ
        Vec3b vec3 = Vec3b(rng.uniform(0, 256), rng.uniform(0, 256), rng.uniform(0, 256));
        colors.push_back(vec3);
    }

    sortrows(stats, stats, CC_STAT_AREA);
    // �����ͨ����ȫ��ͼ���������������stats��һ��Ҫȥ��
    // ����ԭʼ��ͨ�������ʾ���
    img = displayImage(originImage, stats, true, 0);
    imwrite(imagePath + "origin_stats.jpg", img);
    statsWrite(imagePath + "origin_stats.csv", stats);

    // ������ͨ��ϲ�������
    Mat temp;
    combineStats(stats, temp,originImage, 0);
    sortrows(temp, temp, CC_STAT_AREA);
    Mat resImg = displayImage(originImage, temp);
    // ������ͼ
    imwrite(imagePath + "combined_stats.jpg", resImg);
    // ������stats��ͨ���
    statsWrite(imagePath + "combined_stats.csv", temp);

    return 0;
}

// ���г���: Ctrl + F5 ����� >����ʼִ��(������)���˵�
// ���Գ���: F5 ����� >����ʼ���ԡ��˵�

// ����ʹ�ü���: 
//   1. ʹ�ý��������Դ�������������/�����ļ�
//   2. ʹ���Ŷ���Դ�������������ӵ�Դ�������
//   3. ʹ��������ڲ鿴���������������Ϣ
//   4. ʹ�ô����б��ڲ鿴����
//   5. ת������Ŀ��>���������Դ����µĴ����ļ�����ת������Ŀ��>�����������Խ����д����ļ���ӵ���Ŀ
//   6. ��������Ҫ�ٴδ򿪴���Ŀ����ת�����ļ���>���򿪡�>����Ŀ����ѡ�� .sln �ļ�

```