import moment from "moment";

export function dateFormat(date: Date | moment.Moment, absolute: boolean = false): string {
    const val = moment(date);
    if (absolute) {
        if (moment().isSame(val, "day")) {
            return val.format("HH:mm");
        }
        return val.format("DD MMM YYYY HH:mm");
    } else {
        return val.fromNow();
    }
}