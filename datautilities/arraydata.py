import numpy

class InputData(object):

    def __init__(self):
        
        pass
    
    def set_from_data_model(self, data):

        self.set_structure(data)
        self.set_bus(data)
        self.set_sh(data)
        self.set_sd(data)
        self.set_acl(data)
        self.set_dcl(data)
        self.set_xfr(data)
        self.set_prz(data)
        self.set_qrz(data)
        self.set_t(data)
        self.set_k(data)
        self.set_sd_t(data)
        self.set_sd_t_cost(data)

    def set_structure(self, data):

        self.set_num(data)
        self.set_uid(data)
        self.num_all = self.all_uid.size
        self.set_range(data)
        self.set_map(data)
        self.set_type_indicator(data)

    def set_num(self, data):

        self.num_bus = len(data.network.bus)
        self.num_acl = len(data.network.ac_line)
        self.num_dcl = len(data.network.dc_line)
        self.num_xfr = len(data.network.two_winding_transformer)
        self.num_sh = len(data.network.shunt)
        self.num_sd = len(data.network.simple_dispatchable_device)
        self.num_pd = len([i for i in data.network.simple_dispatchable_device if i.device_type == 'producer'])
        self.num_cd = len([i for i in data.network.simple_dispatchable_device if i.device_type == 'consumer'])
        self.num_prz = len(data.network.active_zonal_reserve)
        self.num_qrz = len(data.network.reactive_zonal_reserve)
        self.num_t = len(data.time_series_input.general.interval_duration)
        self.num_k = len(data.reliability.contingency)

    def set_uid(self, data):

        # establish an order of elements in each type
        self.bus_uid = numpy.array([i.uid for i in data.network.bus])
        self.acl_uid = numpy.array([i.uid for i in data.network.ac_line])
        self.dcl_uid = numpy.array([i.uid for i in data.network.dc_line])
        self.xfr_uid = numpy.array([i.uid for i in data.network.two_winding_transformer])
        self.sh_uid = numpy.array([i.uid for i in data.network.shunt])
        self.sd_uid = numpy.array([i.uid for i in data.network.simple_dispatchable_device])
        self.prz_uid = numpy.array([i.uid for i in data.network.active_zonal_reserve])
        self.qrz_uid = numpy.array([i.uid for i in data.network.reactive_zonal_reserve])
        self.k_uid = numpy.array([i.uid for i in data.reliability.contingency])
        self.all_uid = numpy.concatenate((self.bus_uid,
            self.acl_uid,
            self.dcl_uid,
            self.xfr_uid,
            self.sh_uid,
            self.sd_uid,
            self.prz_uid,
            self.qrz_uid,
            self.k_uid))

    def set_range(self, data):

        # ranges
        self.t_num = numpy.array(list(range(self.num_t)))

    def set_map(self, data):

        # maps
        self.bus_map = {self.bus_uid[i]:i for i in range(self.num_bus)}
        self.acl_map = {self.acl_uid[i]:i for i in range(self.num_acl)}
        self.dcl_map = {self.dcl_uid[i]:i for i in range(self.num_dcl)}
        self.xfr_map = {self.xfr_uid[i]:i for i in range(self.num_xfr)}
        self.sh_map = {self.sh_uid[i]:i for i in range(self.num_sh)}
        self.sd_map = {self.sd_uid[i]:i for i in range(self.num_sd)}
        self.prz_map = {self.prz_uid[i]:i for i in range(self.num_prz)}
        self.qrz_map = {self.qrz_uid[i]:i for i in range(self.num_qrz)}
        self.k_map = {self.k_uid[i]:i for i in range(self.num_k)}
        self.all_map = {self.all_uid[i]:i for i in range(self.num_all)}

    def set_type_indicator(self, data):

        # boolean type indicators
        
        start = 0
        end = 0

        end += self.num_bus
        self.all_is_bus = numpy.array([(start <= i and i < end) for i in range(self.num_all)])
        start += self.num_bus

        end += self.num_acl
        self.all_is_acl = numpy.array([(start <= i and i < end) for i in range(self.num_all)])
        start += self.num_acl

        end += self.num_dcl
        self.all_is_dcl = numpy.array([(start <= i and i < end) for i in range(self.num_all)])
        start += self.num_dcl

        end += self.num_xfr
        self.all_is_xfr = numpy.array([(start <= i and i < end) for i in range(self.num_all)])
        start += self.num_xfr

        end += self.num_sh
        self.all_is_sh = numpy.array([(start <= i and i < end) for i in range(self.num_all)])
        start += self.num_sh

        end += self.num_sd
        self.all_is_sd = numpy.array([(start <= i and i < end) for i in range(self.num_all)])
        start += self.num_sd

        end += self.num_prz
        self.all_is_prz = numpy.array([(start <= i and i < end) for i in range(self.num_all)])
        start += self.num_prz

        end += self.num_qrz
        self.all_is_qrz = numpy.array([(start <= i and i < end) for i in range(self.num_all)])
        start += self.num_qrz

        end += self.num_k
        self.all_is_k = numpy.array([(start <= i and i < end) for i in range(self.num_all)])
        start += self.num_k

    def set_bus(self, data):

        data_map = {x.uid:x for x in data.network.bus}
        self.bus_v_max = numpy.array([data_map[i].vm_ub for i in self.bus_uid])
        self.bus_v_min = numpy.array([data_map[i].vm_lb for i in self.bus_uid])
        # active_reserve_uids: List[str] = Field(
        # reactive_reserve_uids: List[str] = Field( # todo
        self.bus_v_0 = numpy.array([data_map[i].initial_status.vm for i in self.bus_uid])
        self.bus_theta_0 = numpy.array([data_map[i].initial_status.va for i in self.bus_uid])

    def set_sh(self, data):

        data_map = {x.uid:x for x in data.network.shunt}
        self.sh_bus_uid = numpy.array([data_map[i].bus for i in self.sh_uid])
        self.sh_bus = numpy.array([self.bus_map[i] for i in self.sh_bus_uid])
        self.sh_g_st = numpy.array([data_map[i].gs for i in self.sh_uid])
        self.sh_b_st = numpy.array([data_map[i].bs for i in self.sh_uid])
        self.sh_u_st_max = numpy.array([data_map[i].step_ub for i in self.sh_uid])
        self.sh_u_st_min = numpy.array([data_map[i].step_lb for i in self.sh_uid])
        self.sh_u_st_0 = numpy.array([data_map[i].initial_status.step for i in self.sh_uid])

    def set_sd(self, data):

        data_map = {x.uid:x for x in data.network.simple_dispatchable_device}
        self.sd_bus_uid = numpy.array([data_map[i].bus for i in self.sd_uid])
        self.sd_bus = numpy.array([self.bus_map[i] for i in self.sd_bus_uid])
        self.sd_is_pr = numpy.array([1 if data_map[i].device_type == 'producer' else 0 for i in self.sd_uid])
        self.sd_is_cs = numpy.array([1 if data_map[i].device_type == 'consumer' else 0 for i in self.sd_uid])
        self.sd_c_su = numpy.array([data_map[i].startup_cost for i in self.sd_uid])
        # startup_states - a list
        self.sd_c_sd = numpy.array([data_map[i].shutdown_cost for i in self.sd_uid])
        # startups_ub - list
        # energy_req_ub - llist
        # energy_req_lb - list
        self.sd_c_on = numpy.array([data_map[i].on_cost for i in self.sd_uid])
        self.sd_d_up_min = numpy.array([data_map[i].in_service_time_lb for i in self.sd_uid])
        self.sd_d_dn_min = numpy.array([data_map[i].down_time_lb for i in self.sd_uid])
        self.sd_p_ramp_up_max = numpy.array([data_map[i].p_ramp_up_ub for i in self.sd_uid])
        self.sd_p_ramp_dn_max = numpy.array([data_map[i].p_ramp_down_ub for i in self.sd_uid])
        self.sd_p_startup_ramp_up_max = numpy.array([data_map[i].p_startup_ramp_ub for i in self.sd_uid])
        self.sd_p_shutdown_ramp_dn_max = numpy.array([data_map[i].p_shutdown_ramp_ub for i in self.sd_uid])
        self.sd_u_on_0 = numpy.array([data_map[i].initial_status.on_status for i in self.sd_uid])
        self.sd_p_0 = numpy.array([data_map[i].initial_status.p for i in self.sd_uid])
        self.sd_q_0 = numpy.array([data_map[i].initial_status.q for i in self.sd_uid])
        self.sd_d_dn_0 = numpy.array([data_map[i].initial_status.accu_down_time for i in self.sd_uid])
        self.sd_d_up_0 = numpy.array([data_map[i].initial_status.accu_up_time for i in self.sd_uid])
        #
        # p-q indicators:
        # self.sd_is_pqe q_linear_cap
        # self.sd_is_pqmax q_bound_cap
        # self.sd_is_pqmin
        #
        # reserves:
        # p_reg_res_up_ub: confloat(gt=-float('inf'), lt=float('inf'), strict=False) = Field(
        # p_reg_res_down_ub: confloat(gt=-float('inf'), lt=float('inf'), strict=False) = Field(
        # p_syn_res_ub: confloat(gt=-float('inf'), lt=float('inf'), strict=False) = Field(
        # p_nsyn_res_ub: confloat(gt=-float('inf'), lt=float('inf'), strict=False) = Field(
        # p_ramp_res_up_online_ub: confloat(gt=-float('inf'), lt=float('inf'), strict=False) = Field(
        # p_ramp_res_down_online_ub: confloat(gt=-float('inf'), lt=float('inf'), strict=False) = Field(
        # p_ramp_res_up_offline_ub: confloat(gt=-float('inf'), lt=float('inf'), strict=False) = Field(
        # p_ramp_res_down_offline_ub: confloat(gt=-float('inf'), lt=float('inf'), strict=False) = Field(
        #
        # optionals:
        # self.sd_q_p0 = numpy.array([data_map[i].q_0 optional    )
        # beta: Optional[confloat(gt=-float('inf'), lt=float('inf'), strict=False)] = Field(
        # q_0_ub: Optional[confloat(gt=-float('inf'), lt=float('inf'), strict=False)] = Field(
        # q_0_lb: Optional[confloat(gt=-float('inf'), lt=float('inf'), strict=False)] = Field(
        # beta_ub: Optional[confloat(gt=-float('inf'), lt=float('inf'), strict=False)] = Field(
        # beta_lb: Optional[confloat(gt=-float('inf'), lt=float('inf'), strict=False)] = Field(
        
    def set_acl(self, data):

        data_map = {x.uid:x for x in data.network.ac_line}
        self.acl_fbus_uid = numpy.array([data_map[i].fr_bus for i in self.acl_uid])
        self.acl_tbus_uid = numpy.array([data_map[i].to_bus for i in self.acl_uid])
        self.acl_fbus = numpy.array([self.bus_map[i] for i in self.acl_fbus_uid])
        self.acl_tbus = numpy.array([self.bus_map[i] for i in self.acl_tbus_uid])
        self.acl_r_sr = numpy.array([data_map[i].r for i in self.acl_uid])
        self.acl_x_sr = numpy.array([data_map[i].x for i in self.acl_uid])
        self.acl_g_sr = self.acl_r_sr / (self.acl_r_sr**2 + self.acl_x_sr**2)
        self.acl_b_sr = - self.acl_x_sr / (self.acl_r_sr**2 + self.acl_x_sr**2)
        self.acl_b_ch = numpy.array([data_map[i].b for i in self.acl_uid])
        self.acl_s_max = numpy.array([data_map[i].mva_ub_nom for i in self.acl_uid])
        self.acl_s_max_ctg = numpy.array([data_map[i].mva_ub_em for i in self.acl_uid])
        self.acl_c_su = numpy.array([data_map[i].connection_cost for i in self.acl_uid])
        self.acl_c_sd = numpy.array([data_map[i].disconnection_cost for i in self.acl_uid])
        self.acl_u_on_0 = numpy.array([data_map[i].initial_status.on_status for i in self.acl_uid])
        self.acl_g_fr = numpy.array([data_map[i].g_fr if data_map[i].additional_shunt == 1 else 0.0 for i in self.acl_uid])
        self.acl_b_fr = numpy.array([data_map[i].b_fr if data_map[i].additional_shunt == 1 else 0.0 for i in self.acl_uid])
        self.acl_g_to = numpy.array([data_map[i].g_to if data_map[i].additional_shunt == 1 else 0.0 for i in self.acl_uid])
        self.acl_b_to = numpy.array([data_map[i].b_to if data_map[i].additional_shunt == 1 else 0.0 for i in self.acl_uid])

    def set_dcl(self, data):

        data_map = {x.uid:x for x in data.network.dc_line}
        self.dcl_fbus_uid = numpy.array([data_map[i].fr_bus for i in self.dcl_uid])
        self.dcl_tbus_uid = numpy.array([data_map[i].to_bus for i in self.dcl_uid])
        self.dcl_fbus = numpy.array([self.bus_map[i] for i in self.dcl_fbus_uid])
        self.dcl_tbus = numpy.array([self.bus_map[i] for i in self.dcl_tbus_uid])
        self.dcl_p_max = numpy.array([data_map[i].pdc_ub for i in self.dcl_uid])
        self.dcl_q_fr_max = numpy.array([data_map[i].qdc_fr_ub for i in self.dcl_uid])
        self.dcl_q_fr_min = numpy.array([data_map[i].qdc_fr_lb for i in self.dcl_uid])
        self.dcl_q_to_max = numpy.array([data_map[i].qdc_to_ub for i in self.dcl_uid])
        self.dcl_q_to_min = numpy.array([data_map[i].qdc_to_lb for i in self.dcl_uid])
        self.dcl_p_0 = numpy.array([data_map[i].initial_status.pdc_fr for i in self.dcl_uid])
        self.dcl_q_fr_0 = numpy.array([data_map[i].initial_status.qdc_fr for i in self.dcl_uid])
        self.dcl_q_to_0 = numpy.array([data_map[i].initial_status.qdc_to for i in self.dcl_uid])

    def set_xfr(self, data):

        data_map = {x.uid:x for x in data.network.two_winding_transformer}
        self.xfr_fbus_uid = numpy.array([data_map[i].fr_bus for i in self.xfr_uid])
        self.xfr_tbus_uid = numpy.array([data_map[i].to_bus for i in self.xfr_uid])
        self.xfr_fbus = numpy.array([self.bus_map[i] for i in self.xfr_fbus_uid])
        self.xfr_tbus = numpy.array([self.bus_map[i] for i in self.xfr_tbus_uid])
        self.xfr_r_sr = numpy.array([data_map[i].r for i in self.xfr_uid])
        self.xfr_x_sr = numpy.array([data_map[i].x for i in self.xfr_uid])
        self.xfr_g_sr = self.xfr_r_sr / (self.xfr_r_sr**2 + self.xfr_x_sr**2)
        self.xfr_b_sr = - self.xfr_x_sr / (self.xfr_r_sr**2 + self.xfr_x_sr**2)
        self.xfr_b_ch = numpy.array([data_map[i].b for i in self.xfr_uid])
        self.xfr_tau_max = numpy.array([data_map[i].tm_ub for i in self.xfr_uid])
        self.xfr_tau_min = numpy.array([data_map[i].tm_lb for i in self.xfr_uid])
        self.xfr_phi_max = numpy.array([data_map[i].ta_ub for i in self.xfr_uid])
        self.xfr_phi_min = numpy.array([data_map[i].ta_lb for i in self.xfr_uid])
        self.xfr_s_max = numpy.array([data_map[i].mva_ub_nom for i in self.xfr_uid])
        self.xfr_s_max_ctg = numpy.array([data_map[i].mva_ub_em for i in self.xfr_uid])
        self.xfr_c_su = numpy.array([data_map[i].connection_cost for i in self.xfr_uid])
        self.xfr_c_sd = numpy.array([data_map[i].disconnection_cost for i in self.xfr_uid])
        self.xfr_u_on_0 = numpy.array([data_map[i].initial_status.on_status for i in self.xfr_uid])
        self.xfr_tau_0 = numpy.array([data_map[i].initial_status.tm for i in self.xfr_uid])
        self.xfr_phi_0 = numpy.array([data_map[i].initial_status.ta for i in self.xfr_uid])
        self.xfr_g_fr = numpy.array([data_map[i].g_fr if data_map[i].additional_shunt == 1 else 0.0 for i in self.xfr_uid])
        self.xfr_b_fr = numpy.array([data_map[i].b_fr if data_map[i].additional_shunt == 1 else 0.0 for i in self.xfr_uid])
        self.xfr_g_to = numpy.array([data_map[i].g_to if data_map[i].additional_shunt == 1 else 0.0 for i in self.xfr_uid])
        self.xfr_b_to = numpy.array([data_map[i].b_to if data_map[i].additional_shunt == 1 else 0.0 for i in self.xfr_uid])

    def set_prz(self, data):

        # todo
        pass

    def set_qrz(self, data):

        # todo
        pass

    def set_t(self, data):

        self.t_d = numpy.array(data.time_series_input.general.interval_duration)

    def set_k(self, data):

        self.k_out_device_uid = numpy.array([k.components[0] for k in data.reliability.contingency])
        self.k_out_device = numpy.array([self.all_map[self.k_out_device_uid[i]] for i in range(self.num_k)])
        self.k_out_is_acl = numpy.array([self.all_is_acl[self.k_out_device[i]] for i in range(self.num_k)])
        self.k_out_is_dcl = numpy.array([self.all_is_dcl[self.k_out_device[i]] for i in range(self.num_k)])
        self.k_out_is_xfr = numpy.array([self.all_is_xfr[self.k_out_device[i]] for i in range(self.num_k)])
        self.k_out_acl = numpy.array([self.acl_map[self.k_out_device_uid[i]] if self.k_out_is_acl[i] else 0 for i in range(self.num_k)])
        self.k_out_dcl = numpy.array([self.dcl_map[self.k_out_device_uid[i]] if self.k_out_is_dcl[i] else 0 for i in range(self.num_k)])
        self.k_out_xfr = numpy.array([self.xfr_map[self.k_out_device_uid[i]] if self.k_out_is_xfr[i] else 0 for i in range(self.num_k)])

    def set_sd_t(self, data):

        data_map = {x.uid:x for x in data.time_series_input.simple_dispatchable_device}
        self.sd_t_u_on_max = numpy.array([data_map[i].on_status_ub for i in self.sd_uid])
        self.sd_t_u_on_min = numpy.array([data_map[i].on_status_lb for i in self.sd_uid])
        self.sd_t_p_max = numpy.array([data_map[i].p_ub for i in self.sd_uid])
        self.sd_t_p_min = numpy.array([data_map[i].p_lb for i in self.sd_uid])
        self.sd_t_q_max = numpy.array([data_map[i].q_ub for i in self.sd_uid])
        self.sd_t_q_min = numpy.array([data_map[i].q_lb for i in self.sd_uid])
        self.sd_t_c_rgu = numpy.array([data_map[i].p_reg_res_up_cost for i in self.sd_uid])
        self.sd_t_c_rgd = numpy.array([data_map[i].p_reg_res_down_cost for i in self.sd_uid])
        self.sd_t_c_scr = numpy.array([data_map[i].p_syn_res_cost for i in self.sd_uid])
        self.sd_t_c_nsc = numpy.array([data_map[i].p_nsyn_res_cost for i in self.sd_uid])
        self.sd_t_c_rru_on = numpy.array([data_map[i].p_ramp_res_up_online_cost for i in self.sd_uid])
        self.sd_t_c_rrd_on = numpy.array([data_map[i].p_ramp_res_down_online_cost for i in self.sd_uid])
        self.sd_t_c_rru_off = numpy.array([data_map[i].p_ramp_res_up_offline_cost for i in self.sd_uid])
        self.sd_t_c_rrd_off = numpy.array([data_map[i].p_ramp_res_down_offline_cost for i in self.sd_uid])
        self.sd_t_c_qru = numpy.array([data_map[i].q_res_up_cost for i in self.sd_uid])
        self.sd_t_c_qrd = numpy.array([data_map[i].q_res_down_cost for i in self.sd_uid])

    def set_sd_t_cost(self, data):

        # todo cost list(list(tuple(float))) - dims = (t, cost_block, block_entry), t = 1...24, cost_block = b1, ..., b5 (e.g.), block_entry = (c, pmax)

        # cost: List[List[Tuple[confloat(gt=-float('inf'), lt=float('inf'), strict=False), confloat(gt=-float('inf'), lt=float('inf'), strict=False)]]] = Field(
        #     title = "cost",
        #     description = "Array of cost blocks, where   each cost block is an array with exactly two elements:     1) marginal cost in \$/p.u.-hr (Float), and 2) block size in p.u. (Float) "
        # )

        pass


class OutputData(object):

    def __init__(self):

        pass

    def set_from_data_model(self, input_data, output_data_model):
        
        self.set_bus_t(input_data, output_data_model)
        self.set_sh_t(input_data, output_data_model)
        self.set_sd_t(input_data, output_data_model)
        self.set_acl_t(input_data, output_data_model)
        self.set_dcl_t(input_data, output_data_model)
        self.set_xfr_t(input_data, output_data_model)

    def set_bus_t(self, input_data, output_data_model):

        data_map = {x.uid:x for x in output_data_model.time_series_output.bus}
        self.bus_t_v = numpy.array([data_map[i].vm for i in input_data.bus_uid])
        self.bus_t_theta = numpy.array([data_map[i].va for i in input_data.bus_uid])

    def set_sh_t(self, input_data, output_data_model):

        data_map = {x.uid:x for x in output_data_model.time_series_output.shunt}
        self.sh_t_u_st = numpy.array([data_map[i].step for i in input_data.sh_uid])

    def set_sd_t(self, input_data, output_data_model):

        data_map = {x.uid:x for x in output_data_model.time_series_output.simple_dispatchable_device}
        self.sd_t_u_on = numpy.array([data_map[i].on_status for i in input_data.sd_uid])
        self.sd_t_p_on = numpy.array([data_map[i].p_on for i in input_data.sd_uid])
        self.sd_t_q = numpy.array([data_map[i].q for i in input_data.sd_uid])
        self.sd_t_p_rgu = numpy.array([data_map[i].p_reg_res_up for i in input_data.sd_uid])
        self.sd_t_p_rgd = numpy.array([data_map[i].p_reg_res_down for i in input_data.sd_uid])
        self.sd_t_p_scr = numpy.array([data_map[i].p_syn_res for i in input_data.sd_uid])
        self.sd_t_p_nsc = numpy.array([data_map[i].p_nsyn_res for i in input_data.sd_uid])
        self.sd_t_p_rru_on = numpy.array([data_map[i].p_ramp_res_up_online for i in input_data.sd_uid])
        self.sd_t_p_rrd_on = numpy.array([data_map[i].p_ramp_res_down_online for i in input_data.sd_uid])
        self.sd_t_p_rru_off = numpy.array([data_map[i].p_ramp_res_up_offline for i in input_data.sd_uid])
        self.sd_t_p_rrd_off = numpy.array([data_map[i].p_ramp_res_down_offline for i in input_data.sd_uid])
        self.sd_t_q_qru = numpy.array([data_map[i].q_res_up for i in input_data.sd_uid])
        self.sd_t_q_qrd = numpy.array([data_map[i].q_res_down for i in input_data.sd_uid])

    def set_acl_t(self, input_data, output_data_model):

        data_map = {x.uid:x for x in output_data_model.time_series_output.ac_line}
        self.acl_t_u_on = numpy.array([data_map[i].on_status for i in input_data.acl_uid]) # , dtype=numpy.int8) # could help, but not much

    def set_dcl_t(self, input_data, output_data_model):

        data_map = {x.uid:x for x in output_data_model.time_series_output.dc_line}
        self.dcl_t_p = numpy.array([data_map[i].pdc_fr for i in input_data.dcl_uid])
        self.dcl_t_q_fr = numpy.array([data_map[i].qdc_fr for i in input_data.dcl_uid])
        self.dcl_t_q_to = numpy.array([data_map[i].qdc_to for i in input_data.dcl_uid])

    def set_xfr_t(self, input_data, output_data_model):

        data_map = {x.uid:x for x in output_data_model.time_series_output.two_winding_transformer}
        self.xfr_t_u_on = numpy.array([data_map[i].on_status for i in input_data.xfr_uid])
        self.xfr_t_tau = numpy.array([data_map[i].tm for i in input_data.xfr_uid])
        self.xfr_t_phi = numpy.array([data_map[i].ta for i in input_data.xfr_uid])

