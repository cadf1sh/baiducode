#include <stdio.h>
#include <stdlib.h>

#define MAX_SIZE 100  // 定义顺序表的最大长度

typedef struct {
    int *data;  // 存储数据的数组指针
    int cur_size;  // 当前顺序表中的元素个数
    int max_size;  // 顺序表的最大长度
} SequenceList;

// 初始化顺序表
void init(SequenceList *list) {
    list->data = (int *) malloc(MAX_SIZE * sizeof(int));
    list->cur_size = 0;
    list->max_size = MAX_SIZE;
}

// 判断顺序表是否为空
int is_empty(SequenceList *list) {
    return list->cur_size == 0;
}

// 判断顺序表是否已满
int is_full(SequenceList *list) {
    return list->cur_size == list->max_size;
}

// 追加元素到顺序表尾部
void append(SequenceList *list, int element) {
    if (is_full(list)) {
        printf("顺序表已满，无法追加元素");
        return;
    }
    list->data[list->cur_size] = element;
    list->cur_size++;
}

// 删除指定位置的元素
void delete(SequenceList *list, int index) {
    if (index < 0 || index >= list->cur_size) {
        printf("删除位置不合法");
        return;
    }
    for (int i = index + 1; i < list->cur_size; i++) {
        list->data[i-1] = list->data[i];
    }
    list->cur_size--;
}

// 获取指定位置的元素
int get(SequenceList *list, int index) {
    if (index < 0 || index >= list->cur_size) {
        printf("获取位置不合法");
        return -1;
    }
    return list->data[index];
}

int main() {
    SequenceList list;
    init(&list);
    append(&list, 1);
    append(&list, 2);
    append(&list, 3);
    delete(&list, 1);
    printf("%d\n", get(&list, 1));  // 输出结果为 3
    return 0;
}