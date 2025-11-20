package date;

import java.util.Date;

public class PeriodMain {

    public static void main(String[] args) {
        Date start = new Date();
        Date end = new Date();

        Period p = new Period(start, end);
        Period2 p2 = new Period2(start, end);

        System.out.println("p.getDateDiff() = " + p.getDateDiff());  // p.getDateDiff() = 0
        System.out.println("p2.getDateDiff() = " + p2.getDateDiff());  // p2.getDateDiff() = 0

        end.setYear(2026);
        System.out.println("p.getDateDiff() = " + p.getDateDiff());  // p.getDateDiff() = 59989680000000
        System.out.println("p2.getDateDiff() = " + p2.getDateDiff());  // p2.getDateDiff() = 0
    }
}
