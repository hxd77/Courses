#ifndef AP_HW1_H
#define AP_HW1_H
#include<vector>
using std::size_t;

namespace algebra{
    using Matrix=std::vector<std::vector<double>>;

    //创建一个n*m的零矩阵
    Matrix zeros(size_t n ,size_t m);

    //创建一个n*m的全1矩阵
    Matrix ones(size_t n ,size_t m);

    //创建一个n*m的矩阵,元素是min到max的随机数
    Matrix random(size_t n ,size_t m, double min, double max);

    //展示矩阵
    void show(const Matrix& matrix);

    //矩阵乘标量c
    Matrix multiply(const Matrix& matrix, double c);
    
    //矩阵相乘
    Matrix multiply(const Matrix& A,const Matrix& matrix2);

    //矩阵加常数
    Matrix sum(const Matrix& matrix, double c);
    
    //矩阵加矩阵
    Matrix sum(const Matrix& matrix1, const Matrix& matrix2);

    //矩阵转置
    Matrix transpose(const Matrix& matrix);

    //关于n行m列的余子式
    Matrix minor(const Matrix&matrix ,size_t n, size_t m);

    //计算输入matrix的行列式
    double determinant(const Matrix& matrix);

    //矩阵的逆
    Matrix inverse(const Matrix& matrix);

    //将matrix1和matrix2沿指定轴连接
    Matrix concatenate(const Matrix& matrix1,const Matrix& matrix2, int axis=0);

    //交换两行
    Matrix ero_swap(const Matrix& matrix, size_t r1, size_t r2);

    //将一行乘以一个常数
    Matrix ero_multiply(const Matrix& matrix,size_t r,double c);

    //将一行乘以一个常数,然后将其加到另一行
    Matrix ero_sum(const Matrix& matrix,size_t r1,double c,size_t r2);

    //上三角矩阵
    Matrix upper_triangular(const Matrix& matrix);
}

#endif //AP_HW1_H
