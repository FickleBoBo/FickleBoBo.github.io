package date;

import java.util.Date;

public final class Period2 {
    private final Date start;
    private final Date end;

    public Period2(Date start, Date end) {
        this.start = new Date(start.getTime());
        this.end = new Date(end.getTime());
    }

    public long getDateDiff() {
        return end.getTime() - start.getTime();
    }
}
