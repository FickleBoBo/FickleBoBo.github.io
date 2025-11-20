package pack1;

public class Test1Main {

    public static void main(String[] args) {
        Animal[] animals = Test1.animals;
        animals[0].bark();  // dog1 barked

        // Test1.animals 배열은 final 키워드로 새로운 참조 할당 방지
//        Test1.animals = new Animal[2];

        // 배열 내부 원소는 상관 X
        animals[0] = new Cat("cat1");
        animals[0].bark();  // cat1 barked
    }
}
