package supplier;

public class Coffee implements Beverage {

    public Coffee() {
        System.out.println("커피 만들기(아주 무거운 작업)");
    }

    @Override
    public String getName() {
        return "커피";
    }
}
