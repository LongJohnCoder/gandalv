
void addFive(int * p) {
    *p = *p + 5;
}

void main() {
    int *t = new int;
    *t = 2;
    addFive(*t);
    assert(*t == 7);
}
