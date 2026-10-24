// SOMX-CORE Cloudflare Gateway (fail-closed)
export default {
  async fetch(request) {
    const url = new URL(request.url);
    if (url.pathname === "/health") {
      return Response.json({ status: "ok", service: "somx-core" });
    }
    const auth = request.headers.get("Authorization");
    if (!auth || !auth.startsWith("Bearer ")) {
      return Response.json({ error: "unauthorized" }, { status: 401 });
    }
    return Response.json({ error: "not implemented" }, { status: 501 });
  },
};
