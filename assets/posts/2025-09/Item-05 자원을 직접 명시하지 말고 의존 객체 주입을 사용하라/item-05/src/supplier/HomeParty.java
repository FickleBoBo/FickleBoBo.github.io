package supplier;

import java.util.function.Supplier;

public class HomeParty {

    public void prepare(boolean isReady, Beverage beverage) {
        System.out.println("HomeParty.prepare 즉시 연산");
        if (!isReady) return;

        System.out.println(beverage.getName() + " 준비 완료");
    }

    public void prepare(boolean isReady, Supplier<? extends Beverage> supplier) {
        System.out.println("HomeParty.prepare 지연 연산");
        if (!isReady) return;

        Beverage beverage = supplier.get();
        System.out.println(beverage.getName() + " 준비 완료");
    }
}
