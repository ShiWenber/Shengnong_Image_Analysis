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