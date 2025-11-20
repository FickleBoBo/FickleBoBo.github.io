public class Grade {

    public static final Grade BASIC = new Grade("BASIC", 10);
    public static final Grade VIP = new Grade("VIP", 20);

    private final String type;
    private final int discountRate;

    private Grade(String type, int discountRate) {
        this.type = type;
        this.discountRate = discountRate;
    }

    public String getType() {
        return type;
    }

    public int getDiscountRate() {
        return discountRate;
    }

    @Override
    public String toString() {
        return "Grade{" +
                "type='" + type + '\'' +
                ", discountRate=" + discountRate +
                '}';
    }
}
