// One member token per plan, kept in localStorage so a refresh doesn't lose your seat.
const key = (planId: string) => `consensus:token:${planId}`;

export function saveToken(planId: string, token: string) {
  try {
    localStorage.setItem(key(planId), token);
  } catch {
    /* private mode etc. */
  }
}

export function getToken(planId: string): string | null {
  try {
    return localStorage.getItem(key(planId));
  } catch {
    return null;
  }
}
