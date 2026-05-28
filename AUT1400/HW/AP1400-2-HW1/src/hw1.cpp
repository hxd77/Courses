#include "hw1.h"

#include<iomanip>
#include<iostream>
#include<random>
#include<vector>

//把std命名空间中的某些名字单独引入当前作用域
using std::cout;
using std::endl;
using std::left;
using std::logic_error;
using std::setprecision;
using std::setw;

namespace algebra{

    Matrix CreateMatrix(size_t n,size_t m,double v){
        if (n<=0||m<=0){
            throw logic_error("wrong col or row\n");
        }
        Matrix x;
        for(int i=0;i<n;i++){
            std::vector<double>vect(m,v); //m个v值
            x.push_back(vect);
        }
        return x;
    }

    Matrix zeros(size_t n ,size_t m){return CreateMatrix(n,m,0);}

    Matrix ones(size_t n ,size_t m){return CreateMatrix(n,m,1);}

    Matrix random(size_t n,size_t m,double min,double max){
        if(min>max){
            throw logic_error("min can't be greater than max\n");
        }
        auto x{zeros(n,m)};  //auto类型推导+花括号初始化
        std::default_random_engine e; //随机数生成器
        std::uniform_real_distribution<double> u(min,max); //均匀分布,生成min-max中数字概率相同

        for(int i=0;i<n;i++){
            for(int j=0;j<m;j++){
                x[i][j]=u(e); //生成随机数
            }
        }
        return x;
    }

    void show(const Matrix&matrix){
        auto m{matrix.size()}; //行数
        auto n{matrix[0].size()}; //列数
        for(int i=0;i<m;i++){
            for(int j=0;j<n;j++){
                cout<<left<<setw(10)<<setprecision(3)<<matrix[i][j]; //左对齐,宽度10,小数点后三位
            }
            cout<<endl;
        }
    }

    Matrix multiply(const Matrix&matrix,double c){
        if(matrix.size()==0){
            return matrix;
        }
        int m=matrix.size();
        int n =matrix[0].size();
        Matrix x{zeros(m,n)};
        for(int i=0;i<m;i++)
        {
            for (int j = 0; j < n;j++)
            {
                x[i][j]=matrix[i][j]*c;
            }
        }
        return x;
    }

    Matrix multiply(const Matrix&matrix1,const Matrix&matrix2){
        if(matrix1.empty()&&matrix2.empty()){
             return Matrix{};
        }

        if(matrix1.empty()||matrix2.empty()){
            throw logic_error("can't multiply empty matrix\n");
        }

        //维度不同
        if(matrix1[0].size()!=matrix2.size()){
            throw logic_error("can't multiply matrix with wrong size\n");
        }

        auto m{matrix1.size()}; //matrix1的行数
        auto n{matrix2[0].size()}; //matrix2的列数

        auto x{zeros(m,n)};
        for(int i=0;i<m;i++){
            for(int j=0;j<n;j++){
                for(int k=0;k<matrix2.size();k++){
                    x[i][j]+=matrix1[i][k]*matrix2[k][j];
                }
            }
        }
        return x;
    }

    Matrix sum(const Matrix&matrix,double c){
        if(matrix.empty()){
            return Matrix{};
        }
        int m=matrix.size();
        int n=matrix[0].size();
        Matrix x{zeros(m,n)};
        for(int i=0;i<m;i++){
            for(int j=0;j<n;j++){
                x[i][j]=matrix[i][j]+c;
            }
        }
        return x;
    }

    Matrix sum(const Matrix&matrix1,const Matrix&matrix2){
        if(matrix1.empty()&&matrix2.empty()){
            return Matrix{};
        }

        if(matrix1.empty()||matrix2.empty()){
            throw logic_error("can't sum empty matrix\n");
        }

        if(matrix1.size()!=matrix2.size()||matrix1[0].size()!=matrix2[0].size()){
            throw logic_error("can't sum matrix with wrong size\n");
        }

        auto m{matrix1.size()};
        auto n{matrix1[0].size()};
        auto x{zeros(m,n)};
        for(int i=0;i<m;i++){
            for(int j=0;j<n;j++){
                x[i][j]=matrix1[i][j]+matrix2[i][j];
            }
        }
        return x;
    }

    Matrix transpose(const Matrix&matrix){
        if(matrix.empty()){
            return Matrix{};
        }
        int m=matrix.size();
        int n=matrix[0].size();
        Matrix x{zeros(n,m)};
        for(int i=0;i<n;i++){
            for(int j=0;j<m;j++){
                x[i][j]=matrix[j][i];
            }
        }
        return x;
    }

    //子矩阵
    Matrix minor(const Matrix&matrix,size_t n,size_t m){
        if(n<0||n>=matrix.size()||m<0||m>=matrix[0].size()){
            throw logic_error("wrong col or row\n");
        }

        Matrix x;
        for(int i=0;i<matrix.size();i++){
            if(i==n){
                continue;
            }
            std::vector<double> y;
            for(int j=0;j<matrix[0].size();j++){
                if(j==m){
                    continue;
                }
                y.push_back(matrix[i][j]);
            }
            x.push_back(y);
        }
        return x;
    }

    //计算行列式|A|
    double determinant(const Matrix&matrix){
        if(matrix.empty()){
            return 1;
        }
        if(matrix.size()!=matrix[0].size()){
            throw logic_error("can't calculate determinant of non-square matrix\n");
        }
        if(matrix.size()==2){
            return (matrix[0][0]*matrix[1][1]-matrix[0][1]*matrix[1][0]);
        }else if(matrix.size()==1){
            return matrix[0][0];
        }else{
            double res=0;
            for(int i=0;i<matrix.size();i++){ //按第一列展开
                res+=matrix[i][0]*pow(-1,i)*determinant(minor(matrix,i,0));
            }
            return res;
        }
        return 0;
    }

    //求矩阵逆A^-1=A*/|A|,其中A*是A的伴随矩阵
    //A_ij=(-1)^(i+j)*M_ij,其中M_ij是A去掉第i行第j列的子矩阵的行列式值
    //A*=[A_11 A_21 A_31
    //     A_12 A_22 A_32
    //     A_13 A_23 A_33]
    Matrix inverse(const Matrix&matrix){
        if(matrix.empty()){
            return Matrix{};
        }
        if(matrix.size()!=matrix[0].size()||determinant(matrix)==0){
            throw logic_error("can't calculate inverse of non-square or singular matrix\n");
        }
        Matrix x{zeros(matrix.size(),matrix.size())};
        for(int i=0;i<matrix.size();i++){
            for(int j=0;j<matrix[0].size();j++){
                x[i][j]=determinant(minor(matrix,i,j))*pow(-1,i+j);
            }
        }
        x=transpose(x);
        return multiply(x,1/determinant(matrix));
    }

    Matrix concatenate(const Matrix&matrix1,const Matrix&matrix2,int axis){
        if(axis==0){
            if (matrix1[0].size()!=matrix2[0].size()){
                throw logic_error("can't concatenate matrix with wrong size\n");
            }
            Matrix x;
            for(int i=0;i<matrix1.size();i++){
                x.push_back(matrix1[i]);
            }
            for(int j=0;j<matrix2.size();j++){
                x.push_back(matrix2[j]);
            }        
            return x;
        }
        if(matrix1.size()!=matrix2.size()){
            throw logic_error("can't concatenate matrix with wrong size\n");
        }
        Matrix x=zeros(matrix1.size(),matrix1[0].size()+matrix2[0].size());
        for(int i=0;i<x.size();i++){
            for(int j=0;j<x[0].size();j++){
                if(j<matrix1[0].size()){
                    x[i][j]=matrix1[i][j];
                }
                else{
                    x[i][j]=matrix2[i][j-matrix1[0].size()];
                }
            }
        }
        return x;
    }

    //交换两行
    Matrix ero_swap(const Matrix&matrix, size_t r1,size_t r2){
        Matrix x;
        auto len(matrix.size());
        if(r1<0||r1>=len||r2<0||r2>=len){
            throw logic_error("wrong row\n");
        }

        for(int i=0;i<len;i++){
            if(i==r1){
                x.push_back(matrix[r2]);
            }
            else if(i==r2){
                x.push_back(matrix[r1]);
            }
            else{
                x.push_back(matrix[i]);
            }
        }
        return x;
    }

    //某行乘以一个非零常数
    Matrix ero_multiply(const Matrix&matrix ,size_t r,double c){
        auto m{matrix.size()};
        auto n{matrix[0].size()};
        Matrix x=zeros(m,n);

        for(int i=0;i<m;i++){
            for(int j=0;j<n;j++){
                if(i==r){
                    x[i][j]=matrix[i][j]*c;
                    continue;
                }
                x[i][j]=matrix[i][j];        
            }
        }
        return x;
    }

    //某行加上另一行的c倍
    Matrix ero_sum(const Matrix&matrix,size_t r1,double c,size_t r2){
        Matrix x=ero_multiply(matrix,r1,1); //复制一个matrix
        for(int i=0;i<matrix[r2].size();i++){
            x[r2][i]+=(x[r1][i]*c);
        }
        return x;
    }

    //辅助函数 第r1*c加到第r2行
    void mul_sum(Matrix&matrix,size_t r1,double c,size_t r2){
        for(int i=0;i<matrix[r2].size();i++){
            matrix[r2][i]+=(matrix[r1][i]*c);
        }
    }
    //上三角
    Matrix upper_triangular(const Matrix&matrix){
        if(matrix.empty()){
            return Matrix{};
        }
        if(matrix.size()!=matrix[0].size()){
            throw logic_error("can't calculate upper triangular of non-square matrix\n");
        }

        Matrix x=ero_multiply(matrix,0,1); //第0行*1，不变
        if(x[0][0]==0){ 
            int row=1;
            while(x[row][0]==0&&row<x.size()){
                row++;
            }
            if(row==x.size()){
                throw logic_error("can't calculate upper triangular of singular matrix\n");
            }
            x=ero_swap(x,0,row); //交换第0行和第row行
        }

        auto m{matrix.size()};

        for(int i=0;i<m;i++){
            for(int j=i+1;j<m;j++){
                mul_sum(x,i,(-x[j][i]/x[i][i]),j); //第i行乘以-x[j][i]/x[i][i]加到第j行，使得第j行第i列为0
            }
        }
        return x;
    }
}//namespace algebra