package pack1;

public class Test2Main {

    public static void main(String[] args) {
        Dog dog1 = new Dog("dog1");
        Dog dog2 = new Dog("dog2");

        Test2 test2 = new Test2(dog1, dog2);
        test2.func();
        // dog1 barked
        // dog2 barked

        // 멤버 배열을 private으로 선언해도 외부에서 객체를 주입하는 형태면 객체 값이 변경될 수 있다.
        dog1.name = "dog3";
        test2.func();
        // dog3 barked
        // dog2 barked
    }
}
