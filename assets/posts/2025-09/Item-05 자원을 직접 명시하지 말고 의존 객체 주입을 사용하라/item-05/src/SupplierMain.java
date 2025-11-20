import supplier.Coffee;
import supplier.HomeParty;
import supplier.Milk;

public class SupplierMain {

    public static void main(String[] args) {
        HomeParty homeParty = new HomeParty();
        boolean isReady = false;

        homeParty.prepare(isReady, new Coffee());
        homeParty.prepare(isReady, new Milk());
        homeParty.prepare(isReady, () -> new Coffee());
        homeParty.prepare(isReady, () -> new Milk());

        // 커피 만들기(아주 무거운 작업)
        // HomeParty.prepare 즉시 연산

        // 우유 만들기(아주 무거운 작업)
        // HomeParty.prepare 즉시 연산

        // HomeParty.prepare 지연 연산

        // HomeParty.prepare 지연 연산

        isReady = true;
        homeParty.prepare(isReady, new Coffee());
        homeParty.prepare(isReady, new Milk());
        homeParty.prepare(isReady, () -> new Coffee());
        homeParty.prepare(isReady, () -> new Milk());

        // 커피 만들기(아주 무거운 작업)
        // HomeParty.prepare 즉시 연산
        // 커피 준비 완료

        // 우유 만들기(아주 무거운 작업)
        // HomeParty.prepare 즉시 연산
        // 우유 준비 완료

        // HomeParty.prepare 지연 연산
        // 커피 만들기(아주 무거운 작업)
        // 커피 준비 완료

        // HomeParty.prepare 지연 연산
        // 우유 만들기(아주 무거운 작업)
        // 우유 준비 완료
    }
}
