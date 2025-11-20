package supplier;

public class Milk implements Beverage {

    public Milk() {
        System.out.println("우유 만들기(아주 무거운 작업)");
    }

    @Override
    public String getName() {
        return "우유";
    }
}
